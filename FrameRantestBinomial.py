#! /usr/bin/python

from Tkinter import *
from ttk import Separator
from Rantest import Rantest
from PlotRandomDist import PlotRandomDist

__author__="remis"
__date__ ="$26-May-2009 22:51:40$"


class FrameRantestBinomial:
    'GUI for randomisation test'
    
    def __init__(self, root):
        root.title('DC Stats for Mac : Randomisation test : binomial data')
        root.geometry('480x700')
        self.createFrame(root)

    def createFrame(self, root):
        'Creates main frame and data input field.'
        frame = Frame(root)
        frame.pack()

        frame.config(background="#dcdcdc") #well, it has to be, right?
        #frame.geometry('480x700')

        message = Message(frame, width=420, text="\n"+Rantest.introd, font=("Helvetica", 12), background="#dcdcdc")
        message.grid(row=0, column=0, rowspan=15, columnspan=4)
        s = Separator(frame, orient=HORIZONTAL)
        s.grid (columnspan=4, sticky=EW)

        frame_s1 = LabelFrame(frame, text="Sample 1", background="#dcdcdc")
        frame_s1.grid(row=16, rowspan=3,  columnspan=4, padx=20, sticky=W)
        Label(frame_s1, text="Successes:", background="#dcdcdc").grid(row=0, column=0, padx=10, pady=10)
        Label(frame_s1, text="Failures:", background="#dcdcdc").grid(row=0, column=2, pady=10)

        frame_s2 = LabelFrame(frame, text="Sample 2", background="#dcdcdc")
        frame_s2.grid(row=20, rowspan=3,  columnspan=4, padx=20, sticky=W)
        Label(frame_s2, text="Successes:", background="#dcdcdc").grid(row=0, column=0, padx=10, pady=10, sticky=E)
        Label(frame_s2, text="Failures:", background="#dcdcdc").grid(row=0, column=2, pady=10)

        e = []
        e1 = Entry(frame_s1, justify=CENTER, width=10)
        e1.grid(row=0, column=1, padx=10)
        e1.insert(END, '3')
        e.append(e1)

        e2 = Entry(frame_s1, justify=CENTER, width=10)
        e2.grid(row=0, column=3, padx=20)
        e2.insert(END, '4')
        e.append(e2)

        e3 = Entry(frame_s2, justify=CENTER, width=10)
        e3.grid(row=0, column=1, padx=10)
        e3.insert(END, '4')
        e.append(e3)

        e4 = Entry(frame_s2, justify=CENTER, width=10)
        e4.grid(row=0, column=3, padx=20)
        e4.insert(END, '5')
        e.append(e4)

        #Label(frame, text="").grid(row=23, column=0, columnspan=2)
        Label(frame, text="Number of randomisations:", background="#dcdcdc").grid(row=24, column=1, columnspan=2, pady=5, sticky=E)

        e5 = Entry(frame, justify=CENTER, width=15)
        e5.grid(row=24, column=3, pady=5, sticky=W)
        e5.insert(END, '5000')
        e.append(e5)

        #Label(frame, text="").grid(row=25, column=0, columnspan=2)
        b1 = Button(frame, text="Calculate", command=self.calback1, highlightbackground="#dcdcdc").grid(row=26, columnspan=4, pady=5)
        #Label(frame, text="").grid(row=27, column=0, columnspan=4)

        txt = Text(frame)
        txt.grid(row=28, column=0, columnspan=4)
        txt.config(width=64, height= 18, font=("Courier", "12"))
        txt.insert(END, "Results will appear here")
        
        #Label(frame, text="").grid(row=29, column=0, columnspan=4)
        b3 = Button(frame, text="Plot Distribution", command=self.calback2, highlightbackground="#dcdcdc").grid(row=40, columnspan=4, pady=10)
        #Label(frame, text="").grid(row=30, column=0, columnspan=4)

        self.frame = frame
        self.e = e
        self.txt = txt



    def calback1(self):
        'Called by button CALCULATE.'
        dict = self.getResult()
        self.showResult(dict)

    def getResult(self):
        'Calls rantest to calculate statistics.'

        e = self.e
        ir1 = int(e[0].get())
        if1 = int(e[2].get())
        ir2 = int(e[1].get())
        if2 = int(e[3].get())
        nran = int(e[4].get())

        n1 = ir1 + if1
        n2 = ir2 + if2

        rnt = Rantest()
        rnt.tTestBinomial(n1, n2, ir1, ir2)
        rnt.doRantestBinomial(n1, n2, ir1, ir2, 2, nran)
        self.randiff = rnt.dict['randiff']
        self.ir1 = rnt.dict['ir1']

        return rnt.dict

    def showResult(self, rntd):
        'Displays calculation results on main frame.'

        self.txt.delete(1.0, END)

        result1 = (rntd['ir1'], rntd['n1'], rntd['p1'], rntd['sd1'], rntd['ir2'], rntd['n2'], rntd['p2'], rntd['sd2'], rntd['p1'] - rntd['p2'])
        self.txt.insert(END, ' Set 1: %d successes out of %d; \
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
        self.txt.insert(END, '\n Observed 2x2 table: \
        \n  Set 1:    %d      %d      %d \
        \n  Set 2:    %d      %d      %d \
        \n  Total:    %d      %d      %d' %result2)

        #result3 = (rnt.tval, rnt.P)
        self.txt.insert(END, '\n Two-sample unpaired test using Gaussian approximation to binomial: \
        \n standard normal deviate = %(tval)f; two tail P = %(P)f.' %rntd)

        #result4 = (rnt.nran, rnt.pg1, rnt.pl1, rnt.ne1, rnt.pe1)
        self.txt.insert(END, '\n %(nran)d randomisations \
        \n P values for difference between sets are: \
        \n  r1 greater than or equal to observed: P = %(pg1)f \
        \n  r1 less than or equal to observed: P = %(pl1)f \
        \n  r1 equal to observed: number = %(ne1)d (P = %(pe1)f)' %rntd)


    def calback2(self):
        'Called by PLOT DISTRIBUTION button'
        PlotRandomDist(self.randiff,0,1,1, self.ir1)


if __name__ == "__main__":
    root=Tk()
    
    frb = FrameRantestBinomial(root)
    root.mainloop()
