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

import dcstats.basic_stats as bs
from dcstats.hedges import Hedges_d
from dcstats.ratio import Ratio
from dcstats.difference import Difference
from dcstats.twosamples import TwoSamples
from dcstats.twosamples import plot_boxplot
from dcstats.twosamples import Sample

from GUI.report import Report 
from GUI import extratabs
from GUI import mydialogs

__author__="remis"
__date__ ="$03-Jan-2010 15:26:00$"


class DCStatsQT(QDialog):
    def __init__(self, parent=None):
        super(DCStatsQT, self).__init__(parent)
        self.setWindowTitle("DC's Statistics Tools")
        main_box = QHBoxLayout()
        
        # Left side: Welcome and Results text box
        left_box = QVBoxLayout()
        left_box.addWidget(WelcomeScreen())
        self.results = ResultBox()
        left_box.addWidget(self.results)

        buttonHBox = QHBoxLayout()
        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self.on_clear)
        buttonHBox.addWidget(clearButton)
        savePrtButton = QPushButton("Save Printout")
        savePrtButton.clicked.connect(self.on_save)
        buttonHBox.addWidget(savePrtButton)
        #saveHTMLButton = QPushButton("Save HTML")
        #saveHTMLButton.clicked.connect(self.on_save_html)
        #buttonHBox.addWidget(saveHTMLButton)
        left_box.addLayout(buttonHBox)

        self.plot_area = QVBoxLayout()
        self.canvas = GraphPlaceholder()
        self.plot_area.addWidget(self.canvas)
        
        # Right side: controls and plot
        right_box = QVBoxLayout()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(OneStopShopTab(self.results, self.canvas), 
                          "One Stop Shop")
        self.tab_widget.addTab(RandomisationContTab(self.results, self.canvas), 
                          "Rantest: two-sample")
        self.tab_widget.addTab(RandomisationBatchTab(self.results, self.canvas), "Rantest: multi")
        self.tab_widget.addTab(extratabs.RandomisationBinTab(self.results), "Rantest: binary")
        #self.tab_widget.addTab(extratabs.FiellerTab(self.results), "Fieller")
        
        self.tab_widget.setFixedWidth(600)
        self.tab_widget.setFixedHeight(400)
        
        right_box.addWidget(self.tab_widget)
        right_box.addLayout(self.plot_area)
        
        quitButton = QPushButton("&Quit")
        quitButton.clicked.connect(self.close)
        quit_box = QHBoxLayout()
        quit_box.addStretch(1)
        quit_box.addWidget(quitButton)
        right_box.addLayout(quit_box)

        main_box.addLayout(left_box)
        main_box.addLayout(right_box)
        self.setLayout(main_box)
        
    def tab_changed(self):
        item = self.plot_area.takeAt(0).widget()
        self.plot_area.removeWidget(item)
        item.deleteLater()
        self.canvas = GraphPlaceholder()
        self.plot_area.addWidget(self.canvas)

    def on_clear(self):
        self.results.clear()
        self.results.append_info()

    def on_save(self):
        try:
            printOutFilename, filt = QFileDialog.getSaveFileName(self,
                    "Save as PRT file...", ".prt",
                    "PRT files (*.prt)")
            fout = open(printOutFilename,'w')
            fout.write(self.results.toPlainText())
            fout.close()
            self.results.append('\nSession saved to printout file:' + printOutFilename)
        except:
            pass

class OneStopShopTab(QWidget):
    def __init__(self, log, canvas, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        self.log = log

        self.canvas = canvas
        self.path = ''
        self.nran = 10000
        self.paired = 0
        
#        layout.addStretch()
        layout1 = QVBoxLayout()
        bt1 = QPushButton("Get data from Excel file")
        bt1.clicked.connect(self.open_file)
        layout1.addWidget(bt1)
        self.label_file = QLabel('No data loaded yet...')
        layout1.addWidget(self.label_file)
        layout.addLayout(layout1)
        
        layout2 = QHBoxLayout()
        self.sample1 = QComboBox()
        self.sample2 = QComboBox()
        layout2.addWidget(self.sample1)
        layout2.addWidget(self.sample2)
        layout.addLayout(layout2)

        layout3 = QHBoxLayout()
        bt5 = QPushButton("Basic statistics of selected samples")
        bt5.clicked.connect(self.get_basic_stats)
        bt2 = QPushButton("Calculate P by randomisation")
        bt2.clicked.connect(self.get_randomisation)
        layout3.addWidget(bt5)
        layout3.addWidget(bt2)
        layout.addLayout(layout3)

        layout4 = QHBoxLayout()
        bt6 = QPushButton("Bootstrap samples")
        bt6.clicked.connect(self.bootstrap_selected_samples)
        bt7 = QPushButton("Q-Q plots")
        bt7.clicked.connect(self.get_qq_plots)
        layout4.addWidget(bt6)
        layout4.addWidget(bt7)
        layout.addLayout(layout4)
        
        layout5 = QHBoxLayout()
        bt3 = QPushButton("Calculate ratio of means")
        bt3.clicked.connect(self.get_ratio)
        bt4 = QPushButton("Calculate difference of means")
        bt4.clicked.connect(self.get_difference)
        layout5.addWidget(bt3)
        layout5.addWidget(bt4)
        layout.addLayout(layout5)

        layout5 = QHBoxLayout()
        layout5.addStretch()
        layout5.addWidget(QLabel("Number of iterations:"))
        self.ed1 = QLineEdit(str(self.nran))
        self.ed1.editingFinished.connect(self.ran_changed)
        #self.ch1 = QCheckBox("&Paired samples?")
        #self.ch1.stateChanged.connect(self.ran_changed)
        layout5.addWidget(self.ed1)
        #layout5.addWidget(self.ch1)
        layout5.addStretch()
        layout.addLayout(layout5)

        bt8 = QPushButton("Process all samples and save HTML report")
        bt8.clicked.connect(self.process_all)
        layout.addWidget(bt8)

    def process_all(self):
        path, fname = os.path.split(self.filename)
        fname = os.path.splitext(fname)[0]
        fname = fname + '_' + self.shname

        new_path = os.path.join(path, fname)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        os.chdir(new_path)

        n = len(self.names)
        report = Report(fname, get_sys_info())
        report.title('Original data:', 1)
        report.paragraph('Number of samples loaded: ' + str(n))
        report.paragraph(str(self.df.describe()))

        fig = plot_boxplot(self.df)
        fname_boxplot_all = fname  + '_boxplot_all.svg'
        fig.savefig(fname_boxplot_all)
        report.image(fname_boxplot_all)
        plt.close(fig)

        self.log.append('\n\nBatch-processing all sample pairs...')

        for i in range(n):
            self.log.append('\nProcessing sample: ' + self.names[i])
            self.log.repaint()

            report.title('\n\n********************', 1)
            report.title('\n*****   ' + self.names[i]  + '   *****', 1) 

            A = self.df.iloc[:, i].dropna().values #.tolist()
            sample = Sample(A)
            sample.run_bootstrap(self.nran)

            fig = sample.plot_bootstrap()
            fname_sample_boot = fname  + '_sample_boot_' + self.names[i] + '.svg'
            fig.set_size_inches(5,4)
            fig.savefig(fname_sample_boot)
            plt.close(fig)

            fig = sample.plot_qq()
            fname_sample_qq = fname  + '_sample_qq_' + self.names[i] + '.svg'
            fig.set_size_inches(5,4)
            fig.savefig(fname_sample_qq)
            plt.close(fig)

            report.two_images(fname_sample_boot, fname_sample_qq)

        for i in range(n-1):
            for j in range(i+1, n):
                self.log.append('\nProcessing: ' + self.names[i] + ' versus ' + self.names[j])
                self.log.repaint()
                df2 = self.df.iloc[:, [i, j]]
                A = self.df.iloc[:, i].dropna().values.tolist()
                B = self.df.iloc[:, j].dropna().values.tolist()

                report.title('\n\n********************', 1)
                report.dataset('\n*****   ' + self.names[i] + ' versus ' + self.names[j] + '   *****', 
                        str(df2.describe()))
                twosamples = TwoSamples(df2, runs=self.nran)
                report.paragraph(str(twosamples.describe_data()))
                fig = plot_boxplot(df2)
                fname_boxplot = fname  + '_boxplot_' + self.names[i] + '_' + self.names[j] + '.svg'
                fig.set_size_inches(5,4)
                fig.savefig(fname_boxplot)
                #report.image(fname_boxplot)
                plt.close(fig)

                rnt = rantest.RantestContinuous(A, B, False)
                rnt.run_rantest(self.nran)
                report.paragraph(str(rnt))
                fig = rnt.plot_rantest()
                fname_boot = fname  + '_rantest_' + self.names[i] + '_' + self.names[j] + '.svg'
                fig.set_size_inches(5,4)
                fig.savefig(fname_boot)
                #report.image(fname_boot)
                plt.close(fig)

                report.two_images(fname_boxplot, fname_boot)


                report.title('\n Ratio:', 1)
                ratio = Ratio(A, B)
                ratio.run_bootstrap(self.nran)
                report.paragraph(str(ratio))
                report.title('\n Reciprocal:', 1)
                recip = Ratio(B, A)
                recip.run_bootstrap(self.nran)
                report.paragraph(str(recip))
                fig = ratio.plot_bootstrap()
                fname_ratio = fname  + '_ratio_boot_' + self.names[i] + '_' + self.names[j] + '.svg'
                fig.set_size_inches(5,4)
                fig.savefig(fname_ratio)
                #report.image(fname_ratio)
                plt.close(fig)

                report.title('\n Difference:', 1)
                diff = Difference(A, B)
                diff.run_bootstrap(self.nran)
                report.paragraph(str(diff))
                fig = diff.plot_bootstrap()
                fname_diff = fname  + '_diff_boot_' + self.names[i] + '_' + self.names[j] + '.svg'
                fig.set_size_inches(5,4)
                fig.savefig(fname_diff)
                #report.image(fname_diff)
                plt.close(fig)
                report.two_images(fname_ratio, fname_diff)
        report.outputhtml()
        self.log.append('\n\nHTML report done.')

    def get_qq_plots(self):
        df2 = self.get_2sample_df()
        twosamples = TwoSamples(df2, runs=self.nran)
        twosamples.plot_qq_plots(self.canvas.figure)
        self.canvas.draw()

    def bootstrap_selected_samples(self):
        df2 = self.get_2sample_df()
        twosamples = TwoSamples(df2, runs=self.nran)
        twosamples.plot_bootstrapped_distributions(self.canvas.figure)
        self.canvas.draw()

    def get_2sample_df(self):
        i = self.sample1.currentIndex()
        j = self.sample2.currentIndex()
        df2 = self.df.iloc[:, [i, j]]
        return df2

    def ran_changed(self):
        #if self.ch1.isChecked():
        #    self.paired = 1
        #else:
        #    self.paired = 0
        self.nran = int(self.ed1.text()) 

    def get_basic_stats(self):
        df2 = self.get_2sample_df()
        twosamples = TwoSamples(df2)
        self.log.append('\n\n********************')
        self.log.append(str(df2.describe()))
        self.log.append(str(twosamples.describe_data()))
        plot_boxplot(df2, self.canvas.figure)
        self.canvas.draw()

    def get_randomisation(self):
        i = self.sample1.currentIndex()
        j = self.sample2.currentIndex()

        A = self.df.iloc[:, i].dropna().values.tolist()
        B = self.df.iloc[:, j].dropna().values.tolist()

        rnt = rantest.RantestContinuous(A, B, False)
        self.log.append(rnt.describe_data())
        rnt.run_rantest(self.nran)
        self.log.append(str(rnt))

        rnt.plot_rantest(self.canvas.figure)
        self.canvas.draw()

    def get_ratio(self):
        i = self.sample1.currentIndex()
        j = self.sample2.currentIndex()

        A = self.df.iloc[:, i].dropna().values.tolist()
        B = self.df.iloc[:, j].dropna().values.tolist()

        self.log.append('\nRatio: ' + self.names[i] + '/' + self.names[j])
        ratio = Ratio(A, B)
        ratio.run_bootstrap(self.nran)
        self.log.append(str(ratio))

        self.log.append('\nReciprocal of ratio: ' + self.names[j] + '/' + self.names[i])
        recip = Ratio(B, A)
        recip.run_bootstrap(self.nran)
        self.log.append(str(recip))

        ratio.plot_bootstrap(self.canvas.figure)
        self.canvas.draw()       

    def get_difference(self):
        i = self.sample1.currentIndex()
        j = self.sample2.currentIndex()

        A = self.df.iloc[:, i].dropna().values.tolist()
        B = self.df.iloc[:, j].dropna().values.tolist()

        self.log.append('\nDifference: ' + self.names[i] + '-' + self.names[j])
        diff = Difference(A, B)
        diff.run_bootstrap(self.nran)
        self.log.append(str(diff))

        diff.plot_bootstrap(self.canvas.figure)
        self.canvas.draw()       

    def open_file(self):
        """Called by TAKE DATA FROM FILE button in Tab2"""
        try:
            self.filename, filt = QFileDialog.getOpenFileName(self,
                "Open Data File...", self.path, "MS Excel Files (*.xlsx)")
            self.path = os.path.split(str(self.filename))[0]
            #TODO: allow loading from other format files
            self.df, self.shname = load_excel_sheet_with_pandas(self.filename)
            self.initiate_shop()
            self.label_file.setText('Loaded: ' + self.filename + '; sheet: ' + self.shname)
            self.log.append('\nData loaded from a file: ' + self.filename +
                            '; sheet: ' + self.shname + '\n')
        except:
            pass

    def initiate_shop(self):
        self.names = self.df.columns.tolist()
        self.sample1.clear() 
        self.sample2.clear() 
        for name in self.names:
            self.sample1.addItem(name)
            self.sample2.addItem(name)
        self.sample2.setCurrentIndex(1)
        plot_boxplot(self.df, self.canvas.figure)
        self.canvas.draw()


class RandomisationBatchTab(QWidget):
    def __init__(self, log, canvas, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(rantest.RTINTROD))
        self.log = log
        self.canvas = canvas
        self.nran = 5000
        self.path = ""

        bt1 = QPushButton("Get data from Excel file")
        layout.addWidget(bt1)
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Number of randomisations:"))
        self.ed1 = QLineEdit(str(self.nran))
        layout1.addWidget(self.ed1)
        layout.addLayout(layout1)
        bt2 = QPushButton("Run randomisation test")
        layout.addWidget(bt2)
        bt1.clicked.connect(self.open_file)
        bt2.clicked.connect(self.run_rantest)

    def open_file(self):
        """Called by TAKE DATA FROM FILE button in Tab2"""
        try:
            self.filename, filt = QFileDialog.getOpenFileName(self,
                "Open Data File...", self.path, "MS Excel Files (*.xlsx)")
            self.path = os.path.split(str(self.filename))[0]
            df, sheet_name = load_excel_sheet_with_pandas(self.filename)
            self.initiate_rantest(df, sheet_name)
        except:
            pass

    def initiate_rantest(self, df, sheet_name):
        # Display basic statistics
        self.log.separate()
        self.log.append('\nData loaded from a file: ' + self.filename + 
                        '; sheet: ' + sheet_name + '\n')
        self.rnt = rantest.RantestBatch(df, self.log)
        self.log.append('Loaded {0:d} samples: '.format(self.rnt.n)) 
        self.log.append(str(self.rnt.df.describe()))

        plot_boxplot(df, self.canvas.figure)
        self.canvas.draw()

    def run_rantest(self):
        self.nran = int(self.ed1.text())
        self.rnt.run_rantest(self.nran)


class RandomisationContTab(QWidget):
    def __init__(self, log, canvas, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        self.log = log
        self.canvas = canvas
        layout.addWidget(QLabel(rantest.RTINTROD))

        self.nran = 5000
        self.paired = 0
        self.path = ""

        bt1 = QPushButton("Get data from Excel file")
        layout.addWidget(bt1)
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Number of randomisations:"))
        self.ed1 = QLineEdit(str(self.nran))
        layout1.addWidget(self.ed1)
        self.ch1 = QCheckBox("&Paired test?")
        layout1.addWidget(self.ch1)
        layout.addLayout(layout1)
        bt2 = QPushButton("Run randomisation test")
        layout.addWidget(bt2)

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
            self.df, self.sheet_name = load_excel_sheet_with_pandas(self.filename)
            self.initiate_rantest()
        except:
            pass

    def initiate_rantest(self):
        # Display basic statistics
        self.log.separate()
        self.log.append('\nData loaded from a file: ' + self.filename + '\n')
        self.X = self.df.iloc[:,0].dropna().values #.tolist()
        self.Y = self.df.iloc[:,1].dropna().values #.tolist()
        self.rnt = rantest.RantestContinuous(self.X, self.Y, self.paired)
        self.log.append(self.rnt.describe_data())

        self.canvas.figure.clf()
        self.ax1 = self.canvas.figure.add_subplot(1, 2, 1)
        names = ['sample 1', 'sample 2']
        self.ax1.boxplot((self.X, self.Y))
        # Add some random "jitter" to the x-axis
        x = np.random.normal(1, 0.04, size=len(self.X))
        self.ax1.plot(x, self.X, '.', alpha=0.4)
        y = np.random.normal(2, 0.04, size=len(self.Y))
        self.ax1.plot(y, self.Y, '.', alpha=0.4)
        plt.setp(self.ax1, xticks=[1, 2], xticklabels=names)
        self.ax1.set_ylabel('measurment values')
        plt.tight_layout()
        self.canvas.draw()

    def run_rantest(self):
        """Called by RUN TEST button in Tab2."""
        self.rnt.run_rantest(self.nran)
        self.log.append(str(self.rnt))
        self.ax2 = self.canvas.figure.add_subplot(1, 2, 2)
        self.ax2.hist(self.rnt.randiff, bins=20)
        self.ax2.axvline(x=self.rnt.dbar, color='r', label='observed difference')
        self.ax2.axvline(x=-self.rnt.dbar, color='r')
        self.ax2.axvline(x=self.rnt.lo95lim, color='k', linestyle='--', label='2.5% limits')
        self.ax2.axvline(x=self.rnt.hi95lim, color='k', linestyle='--')
        self.ax2.set_xlabel('difference between means')
        self.ax2.set_ylabel('frequency')
        self.ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)
        plt.tight_layout()
        self.canvas.draw()


class GraphPlaceholder(FigureCanvas):
    """"""
    def __init__(self, parent=None):
        self.figure = plt.figure()
        FigureCanvas.__init__(self, self.figure)
        self.setFixedHeight(300)
        self.setFixedWidth(600)


class WelcomeScreen(QWidget):
    """"""
    def __init__(self, parent=None):
        super(WelcomeScreen, self).__init__(parent)
        self.setFixedWidth(500)
        self.setFixedHeight(250)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("<p align=left>Welcome to DC's Statistics Tools. "
        "Select a statistical test from the tabs.</p>"))
        self.layout.addWidget(self.movie_screen())
        self.layout.addWidget(QLabel("<p align=right><i>David Colquhoun  </i></p>"))
    
    def movie_screen(self):
        """Set up the gif movie screen."""
        movie_screen = QLabel()
        movie_screen.setStyleSheet("QWidget { background-color: %s }"% "white")
        # expand and center the label
        movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        movie_screen.setAlignment(Qt.AlignCenter)
        movie = QMovie("GUI/dca2.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        movie_screen.setMovie(movie)
        movie.start()
        return movie_screen


class ResultBox(QTextBrowser):
    def __init__(self, parent=None):
        super(ResultBox, self).__init__(parent)
        self.setFixedWidth(500)
        self.setFixedHeight(500)
        self.append_info()

    def append_info(self):
        self.append(get_sys_info())
    
    def separate(self):
        self.append('*' * 10)


def get_sys_info():
    return ("DC-stats version: {0}".format(dcstats.__version__) +
            "\nMachine: {0};  \nSystem: {1};\nSystem Version: {2}".format(socket.gethostname(), sys.platform, sys.version) +
            "\nDate and time of analysis: " + str(datetime.datetime.now())[:19])


def load_excel_sheet_with_pandas(filename):
    """ Load all columns from a selected sheet in Excel file. Uses pandas.
        Return pandas data frame"""
    # TODO: should be moved to dataIO but need to agree on refactoring IO
    xl = pd.ExcelFile(filename)
    dialog = mydialogs.ExcelSheetDlg(xl.sheet_names) #self
    if dialog.exec_():
        xlssheet = dialog.returnSheet()
    df = xl.parse(xlssheet)
    return df, xl.sheet_names[xlssheet]

