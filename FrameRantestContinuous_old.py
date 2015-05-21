#! /usr/bin/python

from Tkinter import *
from Rantest import Rantest
from data_screen import Data_Screen
from PlotRandomDist import PlotRandomDist
from ReadRandat import read_Data

__author__="remis"
__date__ ="$27-May-2009 12:45:34$"

class FrameRantestContinuous(object):
    'GUI for randomisation test'

    def createFrame(self):
        'Creates main frame and data input field.'

        self.frame = Tk()
        self.frame.title('DC_PyPs: Randomisation test: continuously variable data.')
        #self.frame.geometry('420x700')
        message = Message(self.frame, width = 390, text=Rantest.introd)
        message.grid(row=0, column=0, rowspan=15, columnspan=4)
        Label(self.frame, text="Number of randomisations:").grid(row=16, column=0)
        self.e5 = Entry(self.frame, justify=CENTER)
        self.e5.grid(row=16, column=1)
        self.e5.insert(END, '5000')
        self.var1 = IntVar()
        text1="Paired test?"
        c1=Checkbutton(self.frame, text=text1, variable=self.var1).grid(row=16, column=2, columnspan=2)
        Label(self.frame, text="").grid(row=17, column=0, columnspan=2)

        b1 = Button(self.frame, text="GET DATA AND CALCULATE", command=self.callback1).grid(row=21, columnspan=4)
        Label(self.frame, text="").grid(row=22, column=0, columnspan=2)

### NEW BY AP
        b2 = Button(self.frame, text="TAKE DATA FROM .txt FILE", command=self.callback2).grid(row=22, columnspan=4)
        Label(self.frame, text="").grid(row=23, column=0, columnspan=2)
### end of NEW BY AP

        self.txt = Text(self.frame)
        self.txt.grid(row=23, column=0, columnspan=4)
        self.txt.config(width=70, height= 25, font=("Arial", "8", "bold"))
        self.txt.insert(END, "RESULT WILL BE DISPLAYED HERE")

        Label(self.frame, text="").grid(row=(24), column=0, columnspan=4)
        self.b3 = Button(self.frame, text="PLOT  DISTRIBUTION", state=DISABLED, command=self.callback3)
        self.b3.grid(row=(25), columnspan=4)
        Label(self.frame, text="").grid(row=(26), column=0, columnspan=4)

        self.frame.mainloop()

    def callback1(self):
        'Called by GET DATA AND CALCULATE button.'
        in_data, nran = self.getData()
        rntdict = self.getResult(in_data, nran)
        self.showResult(rntdict)

### NEW BY AP
    def callback2(self):
        'Called by TAKE DATA FROM FILE button'
        in_data = read_Data()
        
        self.paired = 1
        self.paired = self.var1.get()
        nran = int(self.e5.get())

        rntdict = self.getResult(in_data, nran)
        self.showResult(rntdict)

### end of NEW BY AP

    def getData(self):
        'Calls a table to enter data manualy.'

        from_screen = Data_Screen(self.frame)
        n1 = from_screen.n1
        n2 = from_screen.n2
        dataScreen = from_screen.data
        data1 = dataScreen[0:n1]
        data2 = dataScreen[n1:n1+n2]

        nset = 1    # number of data sets
        self.paired = 0
        self.paired = self.var1.get()
        nran = int(self.e5.get())

        in_data = []
        in_data.append(nset)
        for j in range(0, nset):
            in_data.append(n1)
            in_data.append(n2)
            titled = 'Set'
            titlex = 'Sample 1'
            titley = 'Sample 2'
            in_data.append(titled)
            in_data.append(titlex)
            in_data.append(titley)
            in_data.append(data1)
            in_data.append(data2)

        return in_data, nran

    def getResult(self, in_data, nran):
        'Calls rantest to calculate statistics.'

        jset = 1
        rnt = Rantest()
        xobs, yobs = rnt.setContinuousData(in_data, nran, jset, self.paired)
        rnt.tTestContinuous(xobs, yobs, self.paired)
        rnt.doRantestContinuous(xobs, yobs, self.paired, nran)
        #rnt.doRantestContinuous(in_data, nran, jset, self.paired)
        self.randiff = rnt.dict['randiff']

        return rnt.dict

    def showResult(self, rntd):
        'Displays calculation results on main frame.'

        self.txt.delete(1.0, END)

        #result1 = (rnt.nx, rnt.ny, rnt.xbar, rnt.ybar, rnt.sdx, rnt.sdy, rnt.sex, rnt.sey)
        self.txt.insert(END, '       n                  %(nx)d                   %(ny)d \
        \n   Mean        %(xbar)f            %(ybar)f \
        \n   s(x), s(y)   %(sdx)f            %(sdy)f \
        \n   s(x/ybar)   %(sex)f            %(sey)f' %rntd)

        if rntd['nx'] == rntd['ny']:
            #result2 = (rnt.dbar, rnt.sdd, rnt.sed)
            self.txt.insert(END, '\n\n Mean difference (dbar) = %(dbar)f \
            \n  s(d) = %(sdd)f; s(dbar) = %(sed)f' %rntd)

        if self.paired:
            #result3 = (rnt.df, rnt.dbar, rnt.sdbar, rnt.tval, rnt.P)
            self.txt.insert(END, '\n\n Paired Student''s t test: \
            \n  t(%(df)d)= %(dbar)f / %(sdbar)f = %(tval)f \
            \n  two tail P = %(P)f' %rntd)
            self.meanToPlot = rntd['dbar']

        else:
            #result4 = (rnt.dobs, rnt.df, rnt.adiff, rnt.sdiff, rnt.tval, rnt.P)
            self.txt.insert(END, '\n\n Observed difference between means= %(dobs)f \
            \n Two-sample unpaired Student''s t test: \
            \n  t(%(df)d) = %(adiff)f / %(sdiff)f = %(tval)f \
            \n  two tail P = %(P)f' %rntd)
            self.meanToPlot = rntd['dobs']

        #result5 = (nran, rnt.pg1, rnt.pl1, rnt.pa1, rnt.ne1, rnt.pe1, rnt.ne2, rnt.pe2)
        self.txt.insert(END, '\n\n   %(nran)d randomisations \
        \n P values for difference between means are: \
        \n  greater than or equal to observed: P = %(pg1)f \
        \n  less than or equal to observed: P = %(pl1)f \
        \n  greater than or equal in absolute value to observed: P = %(pa1)f \
        \n  (Number equal to observed = %(ne1)d (P= %(pe1)f) \
        \n  (Number equal in absolute value to observed = %(ne2)d (P= %(pe2)f)' %rntd)

        self.b3.config(state=NORMAL)

    def callback3(self):
        'Called by PLOT DISTRIBUTION button.'
        PlotRandomDist(self.randiff, self.paired,0,1, self.meanToPlot)

    def __init__(self):
        self.createFrame()

if __name__ == "__main__":
    frc = FrameRantestContinuous()

