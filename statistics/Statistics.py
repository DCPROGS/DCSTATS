#! /usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Rantest import Rantest
from Fieller import Fieller
from ReadRandat import read_Data

__author__="remis"
__date__ ="$03-Jan-2010 15:26:00$"

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
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
        self.rnt = Rantest()

        ####### TAB 1 ##########
        movie_screen = self.movie_screen()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("<p align=center><b>Welcome to DC_PyPs: "
        "Statistics!</b></p>"))
        tab1_layout.addWidget(movie_screen)
        tab1_layout.addWidget(QLabel("<p align=center><b>To continue select a "
        "statistical test from visible tabs.</b></p>"))

        ####### TAB 2 ##########
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout = self.rancont_layout(tab2_layout)

        ####### TAB 3 ##########
        tab3_layout = QVBoxLayout(tab3)
        tab3_layout = self.ranbin_layout(tab3_layout)

        ####### TAB 4 ##########
        tab4_layout = QVBoxLayout(tab4)
        tab4_layout = self.fieller_layout(tab4_layout)

        ##### Finalise main window ######
        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        quitButton = QPushButton("&QUIT")
        self.connect(quitButton, SIGNAL("clicked()"), self, SLOT("close()"))
        vbox.addWidget(quitButton)
        self.setLayout(vbox)
        self.setWindowTitle("DC_PyPs: Statistics")

#######   TAB 4: FIELLER. START  #############
    def fieller_layout(self, tab_layout):
        'Prepare layout for Tab 4. Fieller theorema.'
        
        tab_layout.addWidget(QLabel(Fieller.introd))

        grid = QGridLayout()
        grid.addWidget(QLabel("Nominator:"), 0, 0)
        grid.addWidget(QLabel("SD of Nominator:"), 1, 0)
        grid.addWidget(QLabel("Denominator:"), 2, 0)
        grid.addWidget(QLabel("SD of Denominator:"), 3, 0)
        grid.addWidget(QLabel("Correlation coefficient (nom,denom):"), 4, 0)
        grid.addWidget(QLabel("Student's t value:"), 5, 0)
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
        self.tb4e6 = QLineEdit("2")
        grid.addWidget(self.tb4e6, 5, 1)
        tab_layout.addLayout(grid)

        self.tb4b1 = QPushButton("Calculate")
        tab_layout.addWidget(self.tb4b1)
        self.tb4txt = QTextBrowser()
        self.tb4txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb4txt)
        self.connect(self.tb4b1, SIGNAL("clicked()"), self.callback2)
        
        return tab_layout

    def callback2(self):
        'Called by CALCULATE button in Tab4.'
        flr = self.get_fieller_result()
        self.show_fieller_result(flr.dict)
        
    def get_fieller_result(self):
        'Call Fieller to calculate statistics.'
        a = float(self.tb4e1.text())
        b = float(self.tb4e3.text())
        sa = float(self.tb4e2.text())
        sb = float(self.tb4e4.text())
        r = float(self.tb4e5.text())
        tval = float(self.tb4e6.text())
        flr = Fieller(a, b, sa, sb, r, tval)
        return flr

    def show_fieller_result(self, flrd):
        'Display Fieller calculation results on main frame.'
        self.tb4txt.clear()
        self.tb4txt.append(' Ratio (=a/b) = %(ratio)f \
        \n g = %(g)f \n Confidence limits: lower %(clower)f, upper %(cupper)f \
        \n i.e deviations: lower %(dlow)f, upper %(dhi)f \n Approximate SD of ratio = %(appsd)f \
        \n Approximate CV of ratio = %(cvr)f \n Approximate limits: lower %(applo)f, upper %(apphi)f' %flrd)

#######   TAB 4: FIELLER. END  #############

#######   TAB 3: RANTEST FOR BINARY DATA. START  #############
    def ranbin_layout(self, tab_layout):

        tab_layout.addWidget(QLabel(Rantest.introd))
        tab_layout.addWidget(QLabel("Sample 1"))
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Successes:"))
        self.tb3e1 = QLineEdit("3")
        layout1.addWidget(self.tb3e1)
        layout1.addWidget(QLabel("Failures:"))
        self.tb3e2 = QLineEdit("4")
        layout1.addWidget(self.tb3e2)
        tab_layout.addLayout(layout1)

        tab_layout.addWidget(QLabel("Sample 2"))
        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("Successes:"))
        self.tb3e3 = QLineEdit("4")
        layout2.addWidget(self.tb3e3)
        layout2.addWidget(QLabel("Failures:"))
        self.tb3e4 = QLineEdit("5")
        layout2.addWidget(self.tb3e4)
        tab_layout.addLayout(layout2)

        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("Number of randomisations:"))
        self.tb3e5 = QLineEdit("5000")
        layout3.addWidget(self.tb3e5)
        tab_layout.addLayout(layout3)

        self.tb3b1 = QPushButton("Calculate")
        tab_layout.addWidget(self.tb3b1)
        self.tb3txt = QTextBrowser()
        self.tb3txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb3txt)
        self.connect(self.tb3b1, SIGNAL("clicked()"), self.callback3)

        return tab_layout

    def callback3(self):
        'Called by button CALCULATE.'
        dict = self.get_ranbin_result()
        self.show_ranbin_result(dict)

    def get_ranbin_result(self):
        'Call Rantest to calculate statistics.'

        ir1 = int(self.tb3e1.text())
        if1 = int(self.tb3e2.text())
        ir2 = int(self.tb3e3.text())
        if2 = int(self.tb3e4.text())
        nran = int(self.tb3e5.text())

        n1 = ir1 + if1
        n2 = ir2 + if2

        rnt = Rantest()
        rnt.tTestBinomial(n1, n2, ir1, ir2)
        rnt.doRantestBinomial(n1, n2, ir1, ir2, nran)
        self.randiff = rnt.dict['randiff']
        self.ir1 = rnt.dict['ir1']

        return rnt.dict

    def show_ranbin_result(self, rntd):
       'Display Rantest calculation results on main frame.'

       self.tb3txt.clear()

       result1 = (rntd['ir1'], rntd['n1'], rntd['p1'], rntd['sd1'], rntd['ir2'], rntd['n2'], rntd['p2'], rntd['sd2'], rntd['p1'] - rntd['p2'])
       self.tb3txt.append(' Set 1: %d successes out of %d; \
        \n p1 = %f;   SD(p1) = %f \
        \n Set 2: %d successes out of %d; \
        \n p2 = %f;   SD(p2) = %f \
        \n Observed difference between sets, p1-p2 = %f' %result1)

       if1 = rntd['n1'] - rntd['ir1']
       if2 = rntd['n2'] - rntd['ir2']
       irt = rntd['ir1'] + rntd['ir2']
       ift = rntd['n1'] + rntd['n2'] - rntd['ir1'] - rntd['ir2']
       nt = rntd['n1'] + rntd['n2']

       result2 = (rntd['ir1'], if1, rntd['n1'], rntd['ir2'], if2, rntd['n2'], irt, ift, nt)
       self.tb3txt.append('\n Observed 2x2 table: \
        \n  Set 1:    %d      %d      %d \
        \n  Set 2:    %d      %d      %d \
        \n  Total:    %d      %d      %d' %result2)

        #result3 = (rnt.tval, rnt.P)
       self.tb3txt.append('\n Two-sample unpaired test using Gaussian approximation to binomial: \
        \n standard normal deviate = %(tval)f; two tail P = %(P)f.' %rntd)

        #result4 = (rnt.nran, rnt.pg1, rnt.pl1, rnt.ne1, rnt.pe1)
       self.tb3txt.append('\n %(nran)d randomisations \
        \n P values for difference between sets are: \
        \n  r1 greater than or equal to observed: P = %(pg1)f \
        \n  r1 less than or equal to observed: P = %(pl1)f \
        \n  r1 equal to observed: number = %(ne1)d (P = %(pe1)f)' %rntd)

#######   TAB 3: RANTEST FOR BINARY DATA. END  #############

#######   TAB 2: RANTEST FOR CONTINUOSLY VARIABLY DATA. START  #############
    def rancont_layout(self, tab_layout):
        "Create Tab2 layout."
        tab_layout.addWidget(QLabel(Rantest.introd))

        self.tb2b1 = QPushButton("Get data")
        tab_layout.addWidget(self.tb2b1)

        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Number of randomisations:"))
        self.tb2e5 = QLineEdit(unicode(self.nran))
        layout1.addWidget(self.tb2e5)
        self.tb2c1 = QCheckBox("&Paired test?")
        layout1.addWidget(self.tb2c1)
        tab_layout.addLayout(layout1)

        self.tb2b2 = QPushButton("Run test")
        tab_layout.addWidget(self.tb2b2)
        self.tb2txt = QTextBrowser()
        self.tb2txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb2txt)
        #self.tb2b3 = QPushButton("Plot distribution")
        #tab_layout.addWidget(self.tb2b3)
        self.connect(self.tb2e5, SIGNAL("editingFinished()"), self.ran_changed)
        self.connect(self.tb2c1, SIGNAL("stateChanged(int)"), self.ran_changed)
        self.connect(self.tb2b1, SIGNAL("clicked()"), self.callback1)
        self.connect(self.tb2b2, SIGNAL("clicked()"), self.callback4)
        return tab_layout

    def callback1(self):
        'Called by TAKE DATA FROM FILE button in Tab2'
        self.rancon_data, dfile = read_Data(self)
        #dfile contains source data path and filename
        self.rancon_data_source = 'Data loaded from a text file: '+dfile
        self.get_rancon_result1(self.rancon_data)
        self.show_rancon_result1()
        
    def callback4(self):
        'Called by RUN TEST button in Tab2.'
        self.get_rancon_result2()
        self.show_rancon_result2()

    def get_rancon_result1(self, in_data):
        'Call rantest to calculate statistics.'
        jset = 1    #number of sets. Now implemented only for one set.
        self.rnt = Rantest()
        self.rnt.setContinuousData(self.rancon_data, jset)
        self.rnt.data_statistics()

    def get_rancon_result2(self):
        'Call rantest to calculate t-test and randomisation test.'
        self.rnt.tTestContinuous(self.paired)
        self.rnt.doRantestContinuous(self.paired, self.nran)
        self.randiff = self.rnt.dict['randiff']

    def show_rancon_result1(self):
        'Display data statistics on main frame Tab2.'
        # AP 021209 : many added hard coded tabs ('\t') to ease copy and paste of data
        # First line of output now specifies source file or manual entry

        rntd = self.rnt.dict
        self.tb2txt.clear()
        self.tb2txt.append(self.rancon_data_source+'\n')

        self.tb2txt.append('   n                \t  %(nx)d                \t  %(ny)d \
        \n  Mean       \t %(xbar)f    \t  %(ybar)f \
        \n  s(x), s(y) \t %(sdx)f     \t  %(sdy)f \
        \n  s(x/ybar)  \t %(sex)f     \t  %(sey)f' %rntd)

        if rntd['nx'] == rntd['ny']:
            self.tb2txt.append('\n Mean difference (dbar) = \t %(dbar)f \
            \n  s(d) = \t %(sdd)f \t s(dbar) = \t %(sed)f' %rntd)

    def show_rancon_result2(self):
        'Display randomisation results on main frame Tab2.'

        rntd = self.rnt.dict

        if self.paired:
            self.tb2txt.append('\n Paired Student''s t test: \
            \n  t(%(df)d)= \t %(dbar)f \t / \t%(sdbar)f \t = \t %(tval)f \
            \t  two tail P =\t %(P)f' %rntd)
            self.meanToPlot = rntd['dbar']

        else:
            self.tb2txt.append('\n Observed difference between means= \t %(dobs)f \
            \n Two-sample unpaired Student''s t test: \
            \n t(%(df)d) = \t %(adiff)f / %(sdiff)f = \t %(tval)f \
            \n two tail P = \t %(P)f' %rntd)
            self.meanToPlot = rntd['dobs']

        self.tb2txt.append('\n   %(nran)d randomisations \
        \n P values for difference between means are: \
        \n  greater than or equal to observed: P = \t %(pg1)f \
        \n  less than or equal to observed: P = \t %(pl1)f \
        \n  greater than or equal in absolute value to observed: P = \t %(pa1)f \
        \n  (Number equal to observed = %(ne1)d (P= %(pe1)f) \
        \n  (Number equal in absolute value to observed = %(ne2)d (P= %(pe2)f)' %rntd)

        #self.b3.config(state=NORMAL)

    def ran_changed(self):
        if self.tb2c1.isChecked():
            self.paired = 1
        else:
            self.paired = 0
        #print 'paired=', self.paired

        self.nran = int(self.tb2e5.text())
        #print 'nran=', self.nran
        
#######   TAB 2: RANTEST FOR CONTINUOSLY VARIABLY DATA. START  #############

#######   TAB 1: WELCOME!  START   ############
    def movie_screen(self):
    # set up the gif movie screen
        movie_screen = QLabel()
        # expand and center the label
        movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        movie_screen.setAlignment(Qt.AlignCenter)
        movie = QMovie("dca2.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        movie_screen.setMovie(movie)
        movie.start()
        return movie_screen

#######   TAB 1: WELCOME!  END   ############

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
