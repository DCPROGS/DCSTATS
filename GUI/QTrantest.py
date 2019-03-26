#! /usr/bin/python
import os
import sys
import socket
import datetime
import pandas as pd
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import dcstats
from dcstats import rantest
from dcstats.fieller import Fieller
from dcstats.basic_stats import TTestBinomial

__author__="remis"
__date__ ="$03-Jan-2010 15:26:00$"


class RantestQT(QDialog):
    def __init__(self, parent=None):
        super(RantestQT, self).__init__(parent)
        self.setWindowTitle("DC_PyPs: Statistics")

        main_box = QHBoxLayout()
        # Left side: Result text box
        self.results = ResultBox()
        main_box.addWidget(self.results)       
        # Right side: controls and plot
        self.plot_area = QVBoxLayout()
        self.plot_area.addWidget(WelcomeScreen())
        
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(RandomisationContTab(self.results, self.plot_area), 
                          "Rantest: two-sample")
        self.tab_widget.addTab(RandomisationBatchTab(self.results, self.plot_area), "Rantest: multi")
        self.tab_widget.addTab(RandomisationBinTab(self.results), "Rantest: binary")
        self.tab_widget.addTab(FiellerTab(self.results), "Fieller")
        self.tab_widget.setFixedWidth(600)
        self.tab_widget.currentChanged.connect(self.tab_changed)

        right_box = QVBoxLayout()
        right_box.addWidget(self.tab_widget)
        right_box.addLayout(self.plot_area)
        quitButton = QPushButton("&QUIT")
        quitButton.clicked.connect(self.close)
        right_box.addLayout(single_button(quitButton))
        main_box.addLayout(right_box)
        self.setLayout(main_box)

    def tab_changed(self):
        item = self.plot_area.takeAt(0).widget()
        self.plot_area.removeWidget(item)
        item.deleteLater()
        self.plot_area.addWidget(WelcomeScreen())
        

class FiellerTab(QWidget):
    def __init__(self, log, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        self.log = log

        # Prepare layout for Fieller tab.
        grid = QGridLayout()
        grid.addWidget(QLabel("Nominator:"), 0, 0)
        grid.addWidget(QLabel("SD of Nominator:"), 1, 0)
        grid.addWidget(QLabel("Denominator:"), 2, 0)
        grid.addWidget(QLabel("SD of Denominator:"), 3, 0)
        grid.addWidget(QLabel("Correlation coefficient (nom,denom):"), 4, 0)
        grid.addWidget(QLabel("Alpha:"), 5, 0)
        grid.addWidget(QLabel("Total number of observations (Na + Nb):"), 6, 0)
        self.ed1 = QLineEdit("14")
        grid.addWidget(self.ed1, 0, 1)
        self.ed2 = QLineEdit("3")
        grid.addWidget(self.ed2, 1, 1)
        self.ed3 = QLineEdit("7")
        grid.addWidget(self.ed3, 2, 1)
        self.ed4 = QLineEdit("2")
        grid.addWidget(self.ed4, 3, 1)
        self.ed5 = QLineEdit("0")
        grid.addWidget(self.ed5, 4, 1)
        self.ed6 = QLineEdit("0.05")
        grid.addWidget(self.ed6, 5, 1)
        self.ed7 = QLineEdit("12")
        grid.addWidget(self.ed7, 6, 1)
        layout.addLayout(grid)

        self.bt1 = QPushButton("Calculate SD and confidence limits for a ratio")
        layout.addLayout(single_button(self.bt1))
        self.bt1.clicked.connect(self.calculate_fieller)       

    def calculate_fieller(self):
        'Called by CALCULATE button in Tab4.'
        a = float(self.ed1.text())
        b = float(self.ed3.text())
        sa = float(self.ed2.text())
        sb = float(self.ed4.text())
        r = float(self.ed5.text())
        alpha = float(self.ed6.text())
        Ntot = float(self.ed7.text())
        self.log.separate()
        self.log.append(str(Fieller(a, b, sa, sb, r, alpha, Ntot)))

class RandomisationBinTab(QWidget):
    def __init__(self, log, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        self.log = log
        layout.addWidget(QLabel(rantest.RTINTROD))
        self.nran = 5000

        layout.addWidget(QLabel("Sample 1"))
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Successes:"))
        self.ed1 = QLineEdit("3")
        layout1.addWidget(self.ed1)
        layout1.addWidget(QLabel("Failures:"))
        self.ed2 = QLineEdit("4")
        layout1.addWidget(self.ed2)
        layout1.addStretch()
        layout.addLayout(layout1)

        layout.addWidget(QLabel("Sample 2"))
        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("Successes:"))
        self.ed3 = QLineEdit("4")
        layout2.addWidget(self.ed3)
        layout2.addWidget(QLabel("Failures:"))
        self.ed4 = QLineEdit("5")
        layout2.addWidget(self.ed4)
        layout2.addStretch()
        layout.addLayout(layout2)

        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("Number of randomisations:"))
        self.ed5 = QLineEdit("5000")
        layout3.addWidget(self.ed5)
        layout3.addStretch()
        layout.addLayout(layout3)
        
        self.bt1 = QPushButton("Calculate")
        layout.addLayout(single_button(self.bt1))
        self.bt1.clicked.connect(self.run_rantest_bin)

    def run_rantest_bin(self):
        """Called by button CALCULATE."""
        ir1 = int(self.ed1.text())
        if1 = int(self.ed2.text())
        ir2 = int(self.ed3.text())
        if2 = int(self.ed4.text())
        self.nran = int(self.ed5.text())
        self.log.separate()
        ttb = TTestBinomial(ir1, if1, ir2, if2)
        rnt = rantest.RantestBinomial(ir1, if1, ir2, if2)
        rnt.run_rantest(self.nran)
        self.log.append(str(ttb) + str(rnt))


class RandomisationBatchTab(QWidget):
    def __init__(self, log, plot_area, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(rantest.RTINTROD))
        self.log = log
        self.plot_area = plot_area
        self.nran = 5000
        self.path = ""

        bt1 = QPushButton("Get data from Excel file")
        layout.addLayout(single_button(bt1))
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Number of randomisations:"))
        self.ed1 = QLineEdit(str(self.nran))
        layout1.addWidget(self.ed1)
        layout.addLayout(layout1)
        bt2 = QPushButton("Run randomisation test")
        layout.addLayout(single_button(bt2))
        bt1.clicked.connect(self.open_file)
        bt2.clicked.connect(self.run_rantest)

    def open_file(self):
        """Called by TAKE DATA FROM FILE button in Tab2"""
        try:
            self.filename, filt = QFileDialog.getOpenFileName(self,
                "Open Data File...", self.path, "MS Excel Files (*.xlsx)")
            self.path = os.path.split(str(self.filename))[0]
            #TODO: allow loading from other format files
            df = load_multi_samples_from_excel_with_pandas(self.filename)
        except:
            pass
        self.initiate_rantest(df)

    def initiate_rantest(self, df):
        # Display basic statistics
        self.log.separate()
        self.log.append('\nData loaded from a file: ' + self.filename + '\n')
        self.rnt = rantest.RantestBatch(df, self.log)
        self.log.append('Loaded {0:d} samples: '.format(self.rnt.n)) 
        self.log.append(str(self.rnt.df.describe()))

        item = self.plot_area.takeAt(0).widget()
        self.plot_area.removeWidget(item)
        item.deleteLater()
        self.bbp = RantestBatchPlot(df)
        self.plot_area.addWidget(self.bbp)

    def run_rantest(self):
        self.nran = int(self.ed1.text())
        self.rnt.run_rantest(self.nran)


class RandomisationContTab(QWidget):
    def __init__(self, log, plot_area, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        self.log = log
        self.plot_area = plot_area
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
            self.initiate_rantest()
        except:
            pass
        
    def initiate_rantest(self):
        # Display basic statistics
        self.log.separate()
        self.log.append('\nData loaded from a file: ' + self.filename + '\n')
        self.rnt = rantest.RantestContinuous(self.X, self.Y, self.paired)
        self.log.append(self.rnt.describe_data())

        item = self.plot_area.takeAt(0).widget()
        self.plot_area.removeWidget(item)
        item.deleteLater()
        self.pc = PlotCanvas()
        self.pc.add_boxplot(self.X, self.Y)
        self.plot_area.addWidget(self.pc)

    def run_rantest(self):
        """Called by RUN TEST button in Tab2."""
        self.rnt.run_rantest(self.nran)
        self.log.append(str(self.rnt))
        self.pc.add_randhisto(self.rnt.randiff, self.rnt.dbar, 
                              self.rnt.lo95lim, self.rnt.hi95lim)


class RantestBatchPlot(FigureCanvas):
    """"""
    def __init__(self, df, parent=None):
        self.figure = plt.figure()
        FigureCanvas.__init__(self, self.figure)
        self.setFixedHeight(400)
        self.setFixedWidth(600)
        self.ax1 = self.figure.add_subplot(1, 1, 1)
        self.ax1 = df.boxplot()
        for i in range(df.shape[1]):
            X = df.iloc[:, i].dropna().values.tolist()
            x = np.random.normal(i+1, 0.04, size=len(X))
            self.ax1.plot(x, X, '.', alpha=0.4)
        self.draw()


class PlotCanvas(FigureCanvas):
    """"""
    def __init__(self, parent=None):
        self.figure = plt.figure()
        FigureCanvas.__init__(self, self.figure)
        self.setFixedHeight(400)
        self.setFixedWidth(600)

        self.ax1 = self.figure.add_subplot(1, 2, 1)
        self.ax2 = self.figure.add_subplot(1, 2, 2)

    def add_boxplot(self, X, Y, sample_names=None):
        if sample_names is None:
            names = ['sample 1', 'sample 2']
        else:
            names = sample_names
        self.ax1.clear()
        self.ax1.boxplot((X, Y))
        # Add some random "jitter" to the x-axis
        x = np.random.normal(1, 0.04, size=len(X))
        self.ax1.plot(x, X, '.', alpha=0.4)
        y = np.random.normal(2, 0.04, size=len(Y))
        self.ax1.plot(y, Y, '.', alpha=0.4)
        plt.setp(self.ax1, xticks=[1, 2], xticklabels=names)
        self.ax1.set_ylabel('measurment values')
        plt.tight_layout()
        self.draw()

    def add_randhisto(self, randiff, dbar, lo95lim, hi95lim):
        self.ax2.clear()
        self.ax2.hist(randiff, bins=20)
        self.ax2.axvline(x=dbar, color='r', label='observed difference')
        self.ax2.axvline(x=-dbar, color='r')
        self.ax2.axvline(x=lo95lim, color='k', linestyle='--', label='2.5% limits')
        self.ax2.axvline(x=hi95lim, color='k', linestyle='--')
        self.ax2.set_xlabel('difference between means')
        self.ax2.set_ylabel('frequency')
        self.ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)
        plt.tight_layout()
        self.draw()


class WelcomeScreen(QWidget):
    """"""
    def __init__(self, parent=None):
        super(WelcomeScreen, self).__init__(parent)
        self.setFixedHeight(400)
        self.setStyleSheet("QWidget { background-color: %s }"% "white")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("<p align=center><b>Welcome to DC_PyPs: "
            "Statistics!</b></p>"))
        self.layout.addWidget(self.movie_screen())
        self.layout.addWidget(QLabel("<p align=center><b>To continue select a "
        "statistical test from visible tabs.</b></p>"))

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
        self.setFixedWidth(500)
        self.append("DC-stats version: {0}".format(dcstats.__version__))
        self.append(sys.version)
        self.append("Date and time of analysis: " + str(datetime.datetime.now())[:19])
        self.append("Machine: {0};   System: {1}".format(socket.gethostname(), sys.platform))

    def separate(self):
        self.append('*' * 10)

def ok_cancel_button(parent):
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
    buttonBox.accepted.connect(parent.accept)
    buttonBox.rejected.connect(parent.reject)
    return buttonBox

def single_button(bt):
    b_layout = QHBoxLayout()
    b_layout.addStretch()
    b_layout.addWidget(bt)
    b_layout.addStretch()
    return b_layout

def load_two_samples_from_excel_with_pandas(filename):
    """ Load two columns from a selected sheet in Excel file. 
        Return two samples as lists. """
    # TODO: should be moved to dataIO but need to agree on refactoring IO
    xl = pd.ExcelFile(filename)
    dialog = ExcelSheetDlg(xl.sheet_names) #self
    if dialog.exec_():
        xlssheet = dialog.returnSheet()
    dt = xl.parse(xlssheet)
    X = dt.iloc[:,0].dropna().values.tolist()
    Y = dt.iloc[:,1].dropna().values.tolist()
    return X, Y

def load_multi_samples_from_excel_with_pandas(filename):
    """ Load all columns from a selected sheet in Excel file. Uses pandas.
        Return pandas data frame"""
    # TODO: should be moved to dataIO but need to agree on refactoring IO
    xl = pd.ExcelFile(filename)
    dialog = ExcelSheetDlg(xl.sheet_names) #self
    if dialog.exec_():
        xlssheet = dialog.returnSheet()
    df = xl.parse(xlssheet)
    return df

