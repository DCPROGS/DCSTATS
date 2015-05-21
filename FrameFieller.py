#! /usr/bin/python

from Tkinter import *
from Fieller import Fieller

__author__="remis"
__date__ ="$27-May-2009 20:29:30$"

class FrameFieller(object):
    'GUI for fieller test'

    def createFrame(self):
        'Creates main frame and data input field.'

        frame = Tk()
        frame.title('DC_PyPs - Fieller`s test')
        frame.geometry('480x600')
        message = Message(frame, width = 400, text=Fieller.introd, justify=LEFT)
        message.grid(row=0, column=0, rowspan=15, columnspan=4)

        Label(frame, text="Nominator (a)").grid(row=15, column=1, sticky=E)
        Label(frame, text="SD of Nom. (a)", justify=RIGHT).grid(row=16, column=1, sticky=E)
        Label(frame, text="Denominator (b)").grid(row=17, column=1, columnspan=1, sticky=E)
        Label(frame, text="SD of Denom. (b)").grid(row=18, column=1, sticky=E)
        Label(frame, text="Correlation coefficient (a, b)").grid(row=19, column=0, columnspan=2, sticky=E)
        Label(frame, text="Student's t value").grid(row=20, column=1, sticky=E)
        Label(frame, text="Note: t is the alpha-level deviate from the \nt-distribution for the appropriate degrees of freedom (that is Na + Nb -2)").grid(row=21, column=0, columnspan=4)

        e = []
        e1 = Entry(frame, justify=CENTER)
        e1.grid(row=15, column=2)
        e1.insert(END, '14')
        e.append(e1)
        e2 = Entry(frame, justify=CENTER)
        e2.grid(row=16, column=2)
        e2.insert(END, '3')
        e.append(e2)
        e3 = Entry(frame, justify=CENTER)
        e3.grid(row=17, column=2)
        e3.insert(END, '7')
        e.append(e3)
        e4 = Entry(frame, justify=CENTER)
        e4.grid(row=18, column=2)
        e4.insert(END, '2')
        e.append(e4)
        e5 = Entry(frame, justify=CENTER)
        e5.grid(row=19, column=2)
        e5.insert(END, '0')
        e.append(e5)
        e6 = Entry(frame, justify=CENTER)
        e6.grid(row=20, column=2)
        e6.insert(END, '2')
        e.append(e6)

        b1 = Button(frame, text="Calculate", command=self.calback).grid(row=22, columnspan=4)
        Label(frame, text="").grid(row=23, column=0, columnspan=4)

        txt = Text(frame)
        txt.grid(row=24, column=0, columnspan=4, padx=20)
        txt.config(width=60, height= 8, font=("Courier", "12"))

        self.e = e
        self.txt = txt

        frame.mainloop()

    def calback(self):
        'Called by CALCULATE button.'
        flr = self.getResult()
        self.showResult(flr.dict)

    def getResult(self):
        'Calls fieller to calculate statistics.'

        e = self.e
        a = float(e[0].get())
        b = float(e[2].get())
        sa = float(e[1].get())
        sb = float(e[3].get())
        r = float(e[4].get())
        tval = float(e[5].get())

        flr = Fieller(a, b, sa, sb, r, tval)
        return flr
    
    def showResult(self, flrd):
        'Displays calculation results on main frame.'

        self.txt.delete(1.0, END)
        self.txt.insert(END, ' Ratio (=a/b) = %(ratio)f \
        \n g = %(g)f \n Confidence limits: lower %(clower)f, upper %(cupper)f \
        \n i.e deviations: lower %(dlow)f, upper %(dhi)f \n Approximate SD of ratio = %(appsd)f \
        \n Approximate CV of ratio (%%) = %(cvr)f \n Approximate limits: lower %(applo)f, upper %(apphi)f' %flrd)

    def __init__(self):
        self.createFrame()

if __name__ == "__main__":
    ff = FrameFieller()
