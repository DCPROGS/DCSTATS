#! /usr/bin/python

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dcstats import rantest
from dcstats.fieller import Fieller
from dcstats.basic_stats import TTestBinomial


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

def single_button(bt):
    b_layout = QHBoxLayout()
    b_layout.addStretch()
    b_layout.addWidget(bt)
    b_layout.addStretch()
    return b_layout
