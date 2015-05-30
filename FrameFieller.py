#! /usr/bin/python

from Tkinter import *
from Fieller import Fieller, calc_t

__author__="remis"
__date__ ="$27-May-2009 20:29:30$"

class FrameFieller:
    'GUI for fieller test'
    
    def __init__(self, root):
        
        root.title('DC_PyPs - Fieller`s test')
        root.geometry('480x600')
        print "ff"
        self.createFrame(root)
        #root.mainloop()
    
    def createFrame(self, root):
        'Creates main frame and data input field.'
        

        frame = Frame(root)
        frame.pack()
        message = Message(frame, width = 400, text=Fieller.introd, justify=LEFT)
        message.grid(row=0, column=0, rowspan=15, columnspan=4)

        #label list
        self.ll = ("Nominator (a)", "SD of Nom. (a)", "Denominator (b)", "SD of Denom. (b)", "Correlation coefficient (a, b)", "Alpha-level deviate (e.g. 0.95)", "Total number of observations (Na + Nb)")
        # entry rows 0-6
        self.sample_value = (14, 3, 7, 2, 0, 0.95, 12)
        self.entries = []
        self.sva = []
        #build labels and entry boxes
        for p in self.ll:
            i = len(self.sva)           #i.e. 0 when empty, 1 on next loop
            self.sva.append(StringVar())
            print self.sva
            self.sva[i].trace("w", lambda name, index, mode, var=self.sva[i], i=i: self.entryupdate(var, i))
            Label(frame, text=p).grid(column=0, row=i+15, sticky=E)
            e = Entry(frame, width=6, textvariable=self.sva[i])
            e.grid(column=1, row=i+15)
            
            self.entries.append(e)
            
            self.entries[i].insert(END,str(self.sample_value[i]))
            print self.entries
        
        self.noneditable = ("t value", "degrees of freedom (that is: Na + Nb -2)" )
        # entry rows 7 & 8
        for p in self.noneditable:
            i = len(self.sva)
            self.sva.append(StringVar())
            print self.sva
            self.sva[i].trace("w", lambda name, index, mode, var=self.sva[i], i=i: self.entryupdate(var, i))
            Label(frame, text=p).grid(column=0, row=i+15, sticky=E)
            e = Entry(frame, width=6, textvariable=self.sva[i], state='disabled')
            e.grid(column=1, row=i+15)

        self.dfupdate()
        self.tupdate()
        self.ll = self.ll + self.noneditable

        #Label(frame, text="t value; degrees of freedom (that is: Na + Nb -2)").grid(row=22, column=0)
        
        print "all labels created"
        e = []

        
        b1 = Button(frame, text="Calculate", command=self.calback).grid(row=24, columnspan=4)
        Label(frame, text="").grid(row=25, column=0, columnspan=4)

        txt = Text(frame)
        txt.grid(row=26, column=0, columnspan=4, padx=20)
        txt.config(width=60, height= 8, font=("Courier", "12"))

        self.e = e
        self.txt = txt



    def calback(self):
        'Called by CALCULATE button.'
        flr = self.getResult()
        self.showResult(flr.dict)
    
    def entryupdate(self, sv, i):
        """http://stackoverflow.com/questions/6548837/how-do-i-get-an-event-callback-when-a-tkinter-entry-widget-is-modified"""
        ###Note this code executes when the program starts, because all variables are written...
        print (sv, i, self.ll[i], sv.get())
        #do updating here
        
        #check that alpha is between 0 and 1
        #if self.ll[i] =
        #call calculation of t
        if i == 6: #N therefore df
            self.dfupdate()
            self.tupdate()
        
        elif i == 5: #alpha level
            #self.acheck()
            #self.tupdate()
            pass

        elif i == 4: # correlation coeff
            #self.ccheck()
            pass
                
    def dfupdate(self):
        N = self.sva[6].get()
        try:
            df = int(N) - 2
            if df > 0:
                self.sva[8].set(str(df))
            else:
                self.sva[8].set(str(0))
            
            print ("updated")

        except:
            print("no updating with bad value " + N)
            self.sva[8].set(str(0))

    def tupdate(self):

        df = self.sva[8].get()
        alpha = self.sva[5].get()
        # values have already been checked for validity
        print df, alpha
        tvalue = calc_t(int(df), float(alpha))
        self.sva[7].set(str(tvalue))

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


if __name__ == "__main__":
    root=Tk()
    
    ff = FrameFieller(root)
    root.mainloop()