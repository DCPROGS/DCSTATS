#! /usr/bin/python

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
    from ttk import Separator
    import tkFileDialog
else:
    from tkinter import *
    from tkinter.ttk import Separator
    from tkinter import filedialog as tkFileDialog
    
from dcstats import dataIO
from dcstats.rantest import Rantest
from dcstats.rantest import RantestContinuous
from dcstats.Hedges import Hedges_d
from dcstats.basic_stats import TTestContinuous

from GUI.data_screen import Data_Screen
from GUI.PlotRandomDist import PlotRandomDist

__author__="remis"
__date__ ="$27-May-2009 12:45:34$"

class FrameRantestContinuous:
    'GUI for randomisation test'

    def __init__(self, root):
        root.title('DC Stats for Mac : Randomisation test : continuously variable data.')
        self.createFrame(root)
    
    def createFrame(self, root):
        'Creates main frame and data input field.'
        self.frame = Frame(root)
        self.frame.pack()
        self.frame.config(background="#dcdcdc") #well, it has to be, right?
        
        #self.frame.geometry('600x800')
        message = Message(self.frame, text="\n"+Rantest.introd, justify=LEFT, padx=10, width=500, font=("Helvetica", 12), bg="#dcdcdc")
        message.grid(row=0, column=0, rowspan=6, columnspan=2, sticky=W)

        s = Separator(self.frame, orient=HORIZONTAL)
        s.grid (columnspan=2, sticky=EW)

        Label(self.frame, text="Please select the data source:", justify=LEFT, bg="#dcdcdc").grid(row=15, column=0, padx=10, sticky=W)
        Label(self.frame, text="The calculation will proceed automatically with\n the default number of randomisations (5000).\n\nUse [Repeat Calculation] for more repetitions\n(e.g. to estimate P < 0.001)", font=("Helvetica", 12), justify=LEFT, bg="#dcdcdc").grid(row=15, column=1, rowspan=4, sticky=S)
        self.b1 = Button(self.frame, text="Input data manually", command=self.callback1, highlightbackground="#dcdcdc").grid(row=18, column=0,  sticky=W, padx=30)
        self.b2 = Button(self.frame, text="Generic .txt file", command=self.callback2, highlightbackground="#dcdcdc").grid(row=17, column=0, sticky=W, padx=30)
        self.b3 = Button(self.frame, text="Excel Tab-delimited.txt file", command=self.callback3, highlightbackground="#dcdcdc").grid(row=16, column=0,  sticky=W, padx=30)

        Label(self.frame, text="Number of randomisations:", bg="#dcdcdc").grid(row=22, column=0, padx=30, pady=5, sticky=W)
        #default number of randomizations is 5000
        self.e5 = Entry(self.frame, justify=CENTER, width=12, highlightbackground="#dcdcdc")
        self.e5.grid(row=22, column=1, sticky=W, pady=5)
        self.e5.insert(END, '5000')

        #checkbox for doing a paired test
        self.var1 = IntVar()
        text1="Paired test?"
        self.paired = False
        # Callback is not triggered if checkbox is never touched
        # Hence self.paired is set to zero above.
        c1=Checkbutton(self.frame, text=text1, variable=self.var1, command=self.callback_paired, bg="#dcdcdc").grid(row=23, column=0, padx=30, pady=5, sticky=W)
        
        #checkbox to do bootstrap confidence intervals for Hedges' d
        ###Not implemented yet so check button is disabled
        ###Simple CI are calculated until bootstrap is implemented
        self.var2 = IntVar()
        hedges = "Calculate exact confidence intervals for Hedge's d?"
        self.H_CI = 0
        # Callback will not be triggered if checkbox is never touched
        # Hence self.H_CI is set to zero above.
        c2=Checkbutton(self.frame, text=hedges, state=DISABLED, variable=self.var2, command=self.callback_hedges, bg="#dcdcdc").grid(row=23, column=1, padx=30, pady=5, sticky=W)

        self.txt = Text(self.frame)
        self.txt.grid(row=25, column=0, columnspan=4, padx=10)
        self.txt.config(width=75, height= 25, font=("Courier", "12"))
        self.txt.insert(END, "Results will appear here")
        
        #both these buttons are ungreyed after results are displayed.
        #Label(self.frame, text="").grid(row=(26), column=0, columnspan=4)
        self.b4 = Button(self.frame, text="Repeat calculation", state=DISABLED, command=self.callback4,highlightbackground="#dcdcdc")
        self.b4.grid(row=27, padx=40, pady=10, column=0, sticky=E)
        self.b5 = Button(self.frame, text="Plot Distribution", state=DISABLED, command=self.callback5,highlightbackground="#dcdcdc")
        self.b5.grid(row=27, padx=40, pady=10, column=1, sticky=W)
        
    def read_Data(self, file_type):
        """"Asks for a tab delimited text file or excel tab-delim to use in randomization test.
        file_type :string, can be txt or excel
        """

        data_file_name = tkFileDialog.askopenfilename()
        #Convert file into lines of tab delimited text
        lines_of_file = dataIO.file_read(data_file_name, file_type)

        # Imagine taking a header here, with data titles?

        #Make lines into lists of floating point numbers
        datalines = dataIO.lines_into_traces(lines_of_file)
        data1 = datalines[0]
        data2 = datalines[1]
        return data1, data2, data_file_name

### NEW BY AP
    def callback_paired(self):
        'Called when ""Paired Test?"" tickbox is checked'
        self.paired = self.var1.get()

    def callback_hedges(self):
        'Called when ""Hedges CI"" tickbox is checked'
        self.H_CI= self.var2.get()
        print (self.H_CI)
### end of NEW BY AP

    def callback1(self):
        'Called by GET DATA AND CALCULATE button.'
        self.X, self.Y = self.getData()
        self.getResult()
        
### NEW BY AP
    def callback2(self):
        'Called by TAKE DATA FROM FILE button'
        self.X, self.Y, self.dfile = self.read_Data('txt')
        #dfile contains source data path and filename
        self.data_source = 'Data from ' + self.dfile
        self.e5.delete(0, END)
        self.e5.insert(END, '5000') #reset to low value
        self.getResult()

    def callback3(self):
        'Called by TAKE DATA FROM excel button'
        self.X, self.Y, self.dfile = self.read_Data('excel')
        #dfile contains source data path and filename
        self.data_source = 'Data from ' + self.dfile
        self.e5.delete(0, END)
        self.e5.insert(END, '5000')     #reset to low value
        self.getResult()

    def callback4(self):
        'Called by REPEAT button'
        #self.indata and self.dfile should already be populated.
        #dfile contains source data path and filename
        self.data_source = 'Data from ' + self.dfile       
        self.getResult()

### end of NEW BY AP

    def getData(self):
        'Calls a table to enter data manually.'
        ### NEW BY AP
        self.data_source = 'Data entered by hand'
        ### end of NEW BY AP
        from_screen = Data_Screen(self.frame)
        n1 = from_screen.n1
        n2 = from_screen.n2
        dataScreen = from_screen.data
        data1 = dataScreen[0:n1]
        data2 = dataScreen[n1:n1+n2]
       #number of randomisations
        return data1, data2

    def getResult(self):
        'Calls Rantest and Hedges to calculate statistics.'
        self.nran = int(self.e5.get())
        ttc = TTestContinuous(self.X, self.Y, self.paired)
        rnt = RantestContinuous(self.X, self.Y, self.paired)
        rnt.run_rantest(self.nran)
        self.meanToPlot = rnt.dbar
        self.randiff = rnt.randiff

        #calculation of hedges d and approximate 95% confidence intervals
        #not tested against known values yet AP 170518
        hedges_calculation = Hedges_d(self.X, self.Y)
        hedges_calculation.hedges_d_unbiased()
        #lowerCI, upperCI = hedges_calculation.approx_CI(self.paired)
        #paired needed for degrees of freedom
        lowerCI, upperCI = hedges_calculation.bootstrap_CI(5000)
        #option to have bootstrap calculated CIs should go here
        
        #store results/// NOT NEEDED ANY MORE tidy up later AP
        self.hedges_d = hedges_calculation.d
        self.hedges_lowerCI = lowerCI
        self.hedges_upperCI = upperCI    
        self.showResult(ttc, rnt, hedges_calculation)
    
    def showResult(self, ttc, rnt, hedges):
        'Displays calculation results on main frame.'
        # AP 021209 : hard coded tabs ('\t') ease subsequent copy and paste of results
        # First line of output now specifies source file or manual entry
        self.txt.delete(1.0, END)
        self.txt.insert(END, self.data_source + '\n')
        self.txt.insert(END, ttc)
        print(ttc)
        self.txt.insert(END, rnt)
        self.txt.insert(END, hedges)
        print(rnt)
        print(hedges)
        # results have been calculated, so 'Recalculate' and 'Plot distribution'
        # buttons become available
        self.b4.config(state=NORMAL)
        self.b5.config(state=NORMAL)

    def callback5(self):
        'Called by PLOT DISTRIBUTION button.'
        PlotRandomDist(self.randiff, self.paired,0,1, self.meanToPlot)


if __name__ == "__main__":
    root=Tk()
    frc = FrameRantestContinuous(root)
    root.mainloop()
