#! /usr/bin/python
import os
import sys
import socket
import datetime
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dcstats import helpers
from dcstats import dataIO
from dcstats.fieller import Fieller
import dcstats.rantest as rantest
from dcstats.basic_stats import TTestBinomial

__author__="remis"
__date__ ="$03-Jan-2010 15:26:00$"

class RandomisationContTab(QWidget):
    def __init__(self, log, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        self.log = log
        layout.addWidget(QLabel(rantest.RTINTROD))

        self.nran = 5000
        self.paired = 0
        self.path = ""

        bt1 = QPushButton("Get data from Excel file")
        layout.addLayout(single_button(bt1))
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Number of randomisations:"))
        self.ed1 = QLineEdit(str(self.nran))
        layout1.addWidget(self.ed1)
        self.ch1 = QCheckBox("&Paired test?")
        layout1.addWidget(self.ch1)
        layout.addLayout(layout1)
        bt2 = QPushButton("Run randomisation test")
        layout.addLayout(single_button(bt2))

        self.ed1.editingFinished.connect(self.ran_changed)
        self.ch1.stateChanged.connect(self.ran_changed)
        bt1.clicked.connect(self.open_file)
        bt2.clicked.connect(self.run_rantest)

    def ran_changed(self):
        if self.ch1.isChecked():
            self.paired = 1
        else:
            self.paired = 0
        self.nran = int(self.ed1.text()) 

    def open_file(self):
        """Called by TAKE DATA FROM FILE button in Tab2"""
        try:
            self.filename, filt = QFileDialog.getOpenFileName(self,
                "Open Data File...", self.path, "MS Excel Files (*.xlsx)")
            self.path = os.path.split(str(self.filename))[0]
            #TODO: allow loading from other format files
            self.X, self.Y = load_two_samples_from_excel_with_pandas(self.filename)
            self.get_basic_statistics()
        except:
            pass

    def get_basic_statistics(self):
        # Display basic statistics
        self.log.append('\nData loaded from a file: ' + self.filename + '\n')
        self.log.append(helpers.calculate_ttest_hedges(self.X, self.Y, self.paired))

    def run_rantest(self):
        """Called by RUN TEST button in Tab2."""
        self.log.append(helpers.calculate_rantest_continuous(
            self.nran, self.X, self.Y, self.paired))

class RantestQT(QDialog):
    def __init__(self, parent=None):
        super(RantestQT, self).__init__(parent)
        #self.resize(400, 600)

        main_box = QHBoxLayout()
        # Left side: Result text box
        self.results = ResultBox()
        self.results.setFixedWidth(500)
        main_box.addWidget(self.results)
        
        # Right side: controls and plot
        right_box = QVBoxLayout()
        main_box.addLayout(right_box)
        self.setLayout(main_box)
        self.setWindowTitle("DC_PyPs: Statistics")

        ####### Tabs ##########
        tab_widget = QTabWidget()

        plot_area = QWidget()
        plot_area.setFixedHeight(400)
        plot_area.setStyleSheet("QWidget { background-color: %s }"% "white")
        plot_area_layout = QVBoxLayout(plot_area)
        plot_area_layout.addWidget(QLabel("<p align=center><b>Welcome to DC_PyPs: "
        "Statistics!</b></p>"))
        plot_area_layout.addWidget(self.movie_screen())
        plot_area_layout.addWidget(QLabel("<p align=center><b>To continue select a "
        "statistical test from visible tabs.</b></p>"))
        #tab_widget.addTab(plot_area, "Wellcome!")
        
        tab_widget.addTab(RandomisationContTab(self.results), "Rantest: continuous")

        tab3 = QWidget()
        tab_widget.addTab(tab3, "Rantest: binary")
        self.ranbin_layout(QVBoxLayout(tab3))

        tab4 = QWidget()
        tab_widget.addTab(tab4, "Fieller")
        self.fieller_layout(QVBoxLayout(tab4))

        ##### Finalise main window ######
        
        
        tab_widget.setFixedWidth(600)
        right_box.addWidget(tab_widget)
        right_box.addWidget(plot_area)

        quitButton = QPushButton("&QUIT")
        quitButton.clicked.connect(self.close)
        right_box.addLayout(self.single_button(quitButton))
        #self.setLayout(vbox)

        

#######   TAB 4: FIELLER. START  #############
    def fieller_layout(self, tab_layout):
        'Prepare layout for Tab 4. Fieller theorema.'
        grid = QGridLayout()
        grid.addWidget(QLabel("Nominator:"), 0, 0)
        grid.addWidget(QLabel("SD of Nominator:"), 1, 0)
        grid.addWidget(QLabel("Denominator:"), 2, 0)
        grid.addWidget(QLabel("SD of Denominator:"), 3, 0)
        grid.addWidget(QLabel("Correlation coefficient (nom,denom):"), 4, 0)
        grid.addWidget(QLabel("Alpha:"), 5, 0)
        grid.addWidget(QLabel("Total number of observations (Na + Nb):"), 6, 0)
        self.tb4e1 = QLineEdit("14")
        grid.addWidget(self.tb4e1, 0, 1)
        self.tb4e2 = QLineEdit("3")
        grid.addWidget(self.tb4e2, 1, 1)
        self.tb4e3 = QLineEdit("7")
        grid.addWidget(self.tb4e3, 2, 1)
        self.tb4e4 = QLineEdit("2")
        grid.addWidget(self.tb4e4, 3, 1)
        self.tb4e5 = QLineEdit("0")
        grid.addWidget(self.tb4e5, 4, 1)
        self.tb4e6 = QLineEdit("0.05")
        grid.addWidget(self.tb4e6, 5, 1)
        self.tb4e7 = QLineEdit("12")
        grid.addWidget(self.tb4e7, 6, 1)
        tab_layout.addLayout(grid)

        self.tb4b1 = QPushButton("Calculate SD and confidence limits for a ratio")
        tab_layout.addLayout(self.single_button(self.tb4b1))
        #self.tb4txt = ResultBox()
        #tab_layout.addWidget(self.tb4txt)
        self.tb4b1.clicked.connect(self.callback2)       
        return tab_layout

    def callback2(self):
        'Called by CALCULATE button in Tab4.'
        a = float(self.tb4e1.text())
        b = float(self.tb4e3.text())
        sa = float(self.tb4e2.text())
        sb = float(self.tb4e4.text())
        r = float(self.tb4e5.text())
        alpha = float(self.tb4e6.text())
        Ntot = float(self.tb4e7.text())
        #Call Fieller to calculate statistics.
        flr = Fieller(a, b, sa, sb, r, alpha, Ntot)
        self.results.append(str(flr))
#######   TAB 4: FIELLER. END  #############

#######   TAB 3: RANTEST FOR BINARY DATA. START  #############
    def ranbin_layout(self, tab_layout):
        """ """
        tab_layout.addWidget(QLabel(rantest.RTINTROD))
        tab_layout.addWidget(QLabel("Sample 1"))
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Successes:"))
        self.tb3e1 = QLineEdit("3")
        layout1.addWidget(self.tb3e1)
        layout1.addWidget(QLabel("Failures:"))
        self.tb3e2 = QLineEdit("4")
        layout1.addWidget(self.tb3e2)
        layout1.addStretch()
        tab_layout.addLayout(layout1)

        tab_layout.addWidget(QLabel("Sample 2"))
        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("Successes:"))
        self.tb3e3 = QLineEdit("4")
        layout2.addWidget(self.tb3e3)
        layout2.addWidget(QLabel("Failures:"))
        self.tb3e4 = QLineEdit("5")
        layout2.addWidget(self.tb3e4)
        layout2.addStretch()
        tab_layout.addLayout(layout2)

        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("Number of randomisations:"))
        self.tb3e5 = QLineEdit("5000")
        layout3.addWidget(self.tb3e5)
        layout3.addStretch()
        tab_layout.addLayout(layout3)
        
        self.tb3b1 = QPushButton("Calculate")
        tab_layout.addLayout(self.single_button(self.tb3b1))
        #self.tb3txt = ResultBox()
        #tab_layout.addWidget(self.tb3txt)
        self.tb3b1.clicked.connect(self.callback3)

        return tab_layout

    def callback3(self):
        """Called by button CALCULATE."""
        ir1 = int(self.tb3e1.text())
        if1 = int(self.tb3e2.text())
        ir2 = int(self.tb3e3.text())
        if2 = int(self.tb3e4.text())
        self.nran = int(self.tb3e5.text())
        
        ttb = TTestBinomial(ir1, if1, ir2, if2)
        rnt = rantest.RantestBinomial(ir1, if1, ir2, if2)
        rnt.run_rantest(self.nran)
        self.results.append(str(ttb))
        self.results.append(str(rnt))
        
#######   TAB 3: RANTEST FOR BINARY DATA. END  #############

    def single_button(self, bt):
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(bt)
        b_layout.addStretch()
        return b_layout

#######   TAB 1: WELCOME!  START   ############
    def movie_screen(self):
        """Set up the gif movie screen."""
        movie_screen = QLabel()
        # expand and center the label
        movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        movie_screen.setAlignment(Qt.AlignCenter)
        movie = QMovie("GUI/dca2.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        movie_screen.setMovie(movie)
        movie.start()
        return movie_screen
#######   TAB 1: WELCOME!  END   ############


class ExcelSheetDlg(QDialog):
    """
    Dialog to choose Excel sheet to load.
    """
    def __init__(self, sheetlist, parent=None):
        super(ExcelSheetDlg, self).__init__(parent)
        self.sheet = ''
        self.List = QListWidget()
        self.List.addItems(sheetlist)
        self.List.itemSelectionChanged.connect(self.sheetSelected)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.List)
        layout2 = QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(ok_cancel_button(self))
        self.setLayout(layout2)
        self.resize(200, 300)
        self.setWindowTitle("Choose Excel sheet to load...")

    def sheetSelected(self):
        """
        Get selected sheet name.
        """
        self.sheet = self.List.currentRow()

    def returnSheet(self):
        """
        Return selected sheet name.
        """
        return self.sheet

class ResultBox(QTextBrowser):
    def __init__(self, parent=None):
        super(ResultBox, self).__init__(parent)
        self.append("DC-stats")
        self.append(sys.version)
        self.append("Date and time of analysis: " + str(datetime.datetime.now())[:19])
        self.append("Machine: {0};   System: {1}".format(socket.gethostname(), sys.platform))

def ok_cancel_button(parent):
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
    buttonBox.accepted.connect(parent.accept)
    buttonBox.rejected.connect(parent.reject)
    # Following is for pyqt4
    #self.connect(buttonBox, SIGNAL("accepted()"),
    #     self, SLOT("accept()"))
    #self.connect(buttonBox, SIGNAL("rejected()"),
    #     self, SLOT("reject()"))
    return buttonBox

def single_button(bt):
    b_layout = QHBoxLayout()
    b_layout.addStretch()
    b_layout.addWidget(bt)
    b_layout.addStretch()
    return b_layout

def load_two_samples_from_excel_with_pandas(filename):
    #TODO: currently loads only firs two columns. Allow multiple column load.
    # TODO: consider moving out of this class
    xl = pd.ExcelFile(filename)
    dialog = ExcelSheetDlg(xl.sheet_names) #self
    if dialog.exec_():
        xlssheet = dialog.returnSheet()
    dt = xl.parse(xlssheet)
    X = dt.iloc[:,0].dropna().values.tolist()
    Y = dt.iloc[:,1].dropna().values.tolist()
    return X, Y
