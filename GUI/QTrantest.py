#! /usr/bin/python
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dcstats import dataIO
from dcstats.fieller import Fieller, calc_t
from dcstats.rantest import RantestBinomial
from dcstats.basic_stats import TTestBinomial
from dcstats.rantest import RantestContinuous
from dcstats.Hedges import Hedges_d
from dcstats.basic_stats import TTestContinuous

__author__="remis"
__date__ ="$03-Jan-2010 15:26:00$"

intro_randomisation = '\n RANTEST: performs a randomisation test to compare two \
independent samples. According to the null hypothesis\n \
of no-difference, each outcome would have been the same \
regardless of which group the individual happened to\n \
be allocated. Therefore all N=n1+n2 observations are \
pooled and, as in the actual experiment, divided at random\n \
into groups of size n1 and n2. The fraction \
of randomisations that gives rise to a difference between the groups\n \
at least as large as that observed \
gives the P value.\
\n In the binomial case, in which the measurement is the \
fraction of ''successes'' in each sample (say r1 out of n1, and\n \
r2 out of n2) a ''success'' is given a \
score of 1, ''failure'' = 0.\n'

class rantestQT(QDialog):
    def __init__(self, parent=None):
        super(rantestQT, self).__init__(parent)
        self.resize(400, 600)
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab1.setStyleSheet("QWidget { background-color: %s }"% "white")
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()
        tab_widget.addTab(tab1, "Wellcome!")
        tab_widget.addTab(tab2, "Rantest: continuous")
        tab_widget.addTab(tab3, "Rantest: binary")
        tab_widget.addTab(tab4, "Fieller")

        self.nran = 5000
        self.paired = 0
        self.rancon_data = []
        self.rancon_data_source = ''
        self.path = ""

        ####### Tabs ##########
        movie_screen = self.movie_screen()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("<p align=center><b>Welcome to DC_PyPs: "
        "Statistics!</b></p>"))
        tab1_layout.addWidget(movie_screen)
        tab1_layout.addWidget(QLabel("<p align=center><b>To continue select a "
        "statistical test from visible tabs.</b></p>"))

        tab2_layout = QVBoxLayout(tab2)
        tab2_layout = self.rancont_layout(tab2_layout)

        tab3_layout = QVBoxLayout(tab3)
        tab3_layout = self.ranbin_layout(tab3_layout)

        tab4_layout = QVBoxLayout(tab4)
        tab4_layout = self.fieller_layout(tab4_layout)

        ##### Finalise main window ######
        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        quitButton = QPushButton("&QUIT")
        #self.connect(quitButton, SIGNAL("clicked()"), self, SLOT("close()"))
        quitButton.clicked.connect(self.close)
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(quitButton)
        b_layout.addStretch()
        vbox.addLayout(b_layout)
        self.setLayout(vbox)
        self.setWindowTitle("DC_PyPs: Statistics")

#######   TAB 4: FIELLER. START  #############
    def fieller_layout(self, tab_layout):
        'Prepare layout for Tab 4. Fieller theorema.'
        intro_fieller = ("FIELLER: calculates confidence limits for a ratio " +
            "according Fieller''s theorem." +
            "\nCalculates approximate SD of the ratio r=a/b, given " +
            "the SD of a (numerator) \nand of b (denominator), " +
            "and the correlation coefficient between a, b (zero if they are " +
            "independent). \n")
        tab_layout.addWidget(QLabel(intro_fieller))

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

        self.tb4b1 = QPushButton("Calculate")
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(self.tb4b1)
        b_layout.addStretch()
        tab_layout.addLayout(b_layout)

        self.tb4txt = QTextBrowser()
        self.tb4txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb4txt)
        #self.connect(self.tb4b1, SIGNAL("clicked()"), self.callback2)
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
        df = float(self.tb4e7.text())
        self.tb4txt.clear()
#        log = PrintLog(self.tb4txt) #, sys.stdout)
        #Call Fieller to calculate statistics.
        tval = calc_t(int(df), 1 - float(alpha))
        flr = Fieller(a, b, sa, sb, r, tval)
        self.tb4txt.append(str(flr))
        #dcstats.fieller_printout(a,b, sa, sb, r, tval, output=log)
#######   TAB 4: FIELLER. END  #############

#######   TAB 3: RANTEST FOR BINARY DATA. START  #############
    def ranbin_layout(self, tab_layout):
        """ """
        tab_layout.addWidget(QLabel(intro_randomisation))
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
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(self.tb3b1)
        b_layout.addStretch()
        tab_layout.addLayout(b_layout)

        self.tb3txt = QTextBrowser()
        self.tb3txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb3txt)
        #self.connect(self.tb3b1, SIGNAL("clicked()"), self.callback3)
        self.tb3b1.clicked.connect(self.callback3)

        return tab_layout

    def callback3(self):
        """Called by button CALCULATE."""
        ir1 = int(self.tb3e1.text())
        if1 = int(self.tb3e2.text())
        ir2 = int(self.tb3e3.text())
        if2 = int(self.tb3e4.text())
        nran = int(self.tb3e5.text())
        self.tb3txt.clear()
        
        ttb = TTestBinomial(ir1, if1, ir2, if2)
        rnt = RantestBinomial(ir1, if1, ir2, if2)
        rnt.run_rantest(nran)
        self.tb3txt.append(str(ttb))
        self.tb3txt.append(str(rnt))
        
#######   TAB 3: RANTEST FOR BINARY DATA. END  #############

#######   TAB 2: RANTEST FOR CONTINUOSLY VARIABLY DATA. START  #############
    def rancont_layout(self, tab_layout):
        """Create Tab2 layout."""
        tab_layout.addWidget(QLabel(intro_randomisation))

        self.tb2b1 = QPushButton("Get data")
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(self.tb2b1)
        b_layout.addStretch()
        tab_layout.addLayout(b_layout)

        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Number of randomisations:"))
        self.tb2e5 = QLineEdit(str(self.nran))
        layout1.addWidget(self.tb2e5)
        self.tb2c1 = QCheckBox("&Paired test?")
        layout1.addWidget(self.tb2c1)
        tab_layout.addLayout(layout1)

        self.tb2b2 = QPushButton("Run test")
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(self.tb2b2)
        b_layout.addStretch()
        tab_layout.addLayout(b_layout)

        self.tb2txt = QTextBrowser()
        self.tb2txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb2txt)
        #self.tb2b3 = QPushButton("Plot distribution")
        #tab_layout.addWidget(self.tb2b3)
        #self.connect(self.tb2e5, SIGNAL("editingFinished()"), self.ran_changed)
        self.tb2e5.editingFinished.connect(self.ran_changed)
        #self.connect(self.tb2c1, SIGNAL("stateChanged(int)"), self.ran_changed)
        self.tb2c1.stateChanged.connect(self.ran_changed)
        #self.connect(self.tb2b1, SIGNAL("clicked()"), self.callback1)
        self.tb2b1.clicked.connect(self.callback1)
        #self.connect(self.tb2b2, SIGNAL("clicked()"), self.callback4)
        self.tb2b2.clicked.connect(self.callback4)
        return tab_layout

    def callback1(self):
        """Called by TAKE DATA FROM FILE button in Tab2"""
        filename, filt = QFileDialog.getOpenFileName(self,
            "Open Data File...", self.path, "Text Data Files (*.txt)")
        self.path = os.path.split(str(filename))[0]
        
        lines_of_file = dataIO.file_read(filename, 'txt')
        datalines = dataIO.lines_into_traces(lines_of_file)
        self.X = datalines[0]
        self.Y = datalines[1]
        
        self.tb2txt.clear()
        self.tb2txt.append('Data loaded from a text file: ' + filename + '\n')
        ttc = TTestContinuous(self.X, self.Y, self.paired)
        self.tb2txt.append(str(ttc))
                
    def callback4(self):
        """Called by RUN TEST button in Tab2."""
        rnt = RantestContinuous(self.X, self.Y, self.paired)
        rnt.run_rantest(self.nran)
        self.tb2txt.append(str(rnt))

    def ran_changed(self):
        if self.tb2c1.isChecked():
            self.paired = 1
        else:
            self.paired = 0
        self.nran = int(self.tb2e5.text())
#######   TAB 2: RANTEST FOR CONTINUOSLY VARIABLY DATA. START  #############

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


#class PrintLog:
#    """
#    Write stdout to a QTextEdit.
#    out1 = QTextEdit, QTextBrowser, etc.
#    out2 = sys.stdout, file, etc.
#    """
#    def __init__(self, out1, out2=None):
#        self.out1 = out1
#        self.out2 = out2
#    def write(self, text):
#        self.out1.append(text.rstrip('\n'))
#        if self.out2:
#            self.out2.write(text)
