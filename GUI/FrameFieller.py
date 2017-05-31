#! /usr/bin/python

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
    from ttk import Separator
else:
    from tkinter import *
    from tkinter.ttk import Separator

from dcstats.fieller import Fieller, calc_t

__author__="remis"
__date__ ="$27-May-2009 20:29:30$"

class FrameFieller:
    'GUI for fieller test'
    
    def __init__(self, root):
        
        root.title("DC Stats for Mac - Fieller's test")
        root.geometry('420x600')
        root.config(background="#dcdcdc")
        #print "ff"
        self.createFrame(root)
    
    def createFrame(self, root):
        'Creates main frame and data input field.'

        frame = Frame(root)
        frame.pack()
        frame.config(background="#dcdcdc") #well, it has to be, right?

        message = Message(frame, width = 350, text="\n"+Fieller.introd, justify=LEFT, font=("Helvetica", "11"), background="#dcdcdc")
        message.grid(row=0, column=0, rowspan=10, columnspan=4)

        s = Separator(frame, orient=HORIZONTAL)
        s.grid (columnspan=4, sticky=EW)
        # label list for the editable entryboxes
        # entry rows 0-6
        self.ll = ("Nominator (a)", "SD of Nom. (a)", "Denominator (b)", "SD of Denom. (b)", "Correlation coefficient (a, b)", "Alpha", "Total number of observations (Na + Nb)")
        self.sample_value = (14, 3, 7, 2, 0, 0.05, 12)

        self.entries = []
        self.sva = []
        #build labels and entry boxes
        for p in self.ll:
            i = len(self.sva)           #i.e. 0 when empty, 1 on next loop
            self.sva.append(StringVar())
            #print self.sva
            self.sva[i].trace("w", lambda name, index, mode, var=self.sva[i], i=i: self.entryupdate(var, i))
            Label(frame, text=p, bg="#dcdcdc").grid(column=0, row=i+12, sticky=E)
            e = Entry(frame, width=8, textvariable=self.sva[i], highlightbackground="#dcdcdc")
            e.grid(column=1, row=i+12)
            
            self.entries.append(e)
            
            self.entries[i].insert(END,str(self.sample_value[i]))
            #print self.entries
        
        #Label(frame, text="", bg="#dcdcdc", font=("Helvetica", "11")).grid(column=0, columnspan=2, row=20, sticky=E)
    
        
        lframe = LabelFrame(root, text="Calculated", background="#dcdcdc", padx=20, pady=2)

        self.noneditable = ("Degrees of freedom (Na + Nb - 2)", "Two-tailed t value")
        # entry rows 7 & 8
        for p in self.noneditable:
            i = len(self.sva)
            self.sva.append(StringVar())
            #print self.sva
            self.sva[i].trace("w", lambda name, index, mode, var=self.sva[i], i=i: self.entryupdate(var, i))
            Label(lframe, text=p, bg="#dcdcdc").grid(column=0, row=i, padx=5, pady=3, sticky=E)
            e = Label(lframe, width=8, textvariable=self.sva[i], anchor="w", highlightbackground="black", relief=SUNKEN)
            e.grid(column=1, row=i, padx=5, pady=3)
        
        lframe.pack(padx=10, pady=2)
        
        self.ll = self.ll + self.noneditable
        self.dfupdate()
        self.tupdate()
        
        

        tframe = Frame(root, background="#dcdcdc")
        tframe.pack()
        b1 = Button(tframe, text="Calculate", command=self.calback, highlightbackground="#dcdcdc").grid(row=1, columnspan=4)
        Label(tframe, text="", background="#dcdcdc").grid(row=2, column=0, columnspan=4)
        txt = Text(tframe)
        txt.grid(row=3, column=0, columnspan=4, padx=20)
        txt.config(width=60, height=9, font=("Courier", "11"))
        txt.insert(END, "Results will appear here")

        print ("fieller frame GUI created")
        self.txt = txt


    def calback(self):
        'Called by CALCULATE button.'
        flr = self.getResult()
        self.showResult(flr)
    
    def entryupdate(self, sv, i):
        """http://stackoverflow.com/questions/6548837/how-do-i-get-an-event-callback-when-a-tkinter-entry-widget-is-modified"""
        ###Note this code executes when the program starts, because all variables are written...
        #print (sv, i, self.ll[i], sv.get())
        
        # call calculation of t if N therefore df was changed
        # checks on length of sva are to avoid update errors before GUI is fully constructed
        if i == 6 and len(self.sva) > 7:
            self.dfupdate()
            if self.sva[7].get() == "0":             #df must be more that 0
                self.sva[8].set("n.d.")
            else:
                self.tupdate()
    
        # check that, if updated, alpha is between 0 and 1
        elif i == 5 and len(self.sva) > 7 :
            self.check(i)
            if self.sva[7].get() == "0":             #df must be more that 0
                self.sva[8].set("n.d.")
            else:
                self.tupdate()
        
        # check that, if updated, correlation is between 0 and 1
        elif i == 4:
            self.check(i)
                
    def dfupdate(self):
        N = self.sva[6].get()
        try:
            df = int(N) - 2
            if df > 0:
                self.sva[7].set(str(df))
            else:
                self.sva[7].set(str(0))
            
            print ("updated")

        except:
            #presumably a entry that could not be converted to an integer
            print("no updating with bad value " + N)
            self.sva[7].set(str(0))
    
    def check(self,i):
        entry_ = self.sva[i].get()
        try:
            p = float(entry_)
            if p < 0:
                self.sva[i].set('0.')
            elif p >= 1:
                self.sva[i].set('0.')
        except:
            self.sva[i].set('0.')
    
    
    def tupdate(self):

        df = self.sva[7].get()
        alpha = self.sva[5].get()
        # values have already been checked for validity
        two_tail = 1 - float(alpha)
        print (df, alpha, two_tail)
        
        tvalue = calc_t(int(df), two_tail )
        t_str = ("{:.5f}".format(tvalue))
        self.sva[8].set(t_str)

    def getResult(self):
        'Calls fieller to calculate statistics.'

        a = float(self.sva[0].get())
        b = float(self.sva[2].get())
        sa = float(self.sva[1].get())
        sb = float(self.sva[3].get())
        r = float(self.sva[4].get())
        tval = float(self.sva[8].get())
        #self.input = (a, b, sa, sb, r, tval)

        return Fieller(a, b, sa, sb, r, tval)
    
    def showResult(self, flr):
        'Displays calculation results on main frame.'
        print(flr)
        self.txt.delete(1.0, END)
        if flr.cvr != 0:
            self.txt.insert(END, flr)
            #self.txt.insert(END, ' Ratio (=a/b) = %(ratio)f \
            #\n g = %(g)f \n Confidence limits: lower %(clower)f, upper %(cupper)f \
            #\n i.e deviations: lower %(dlow)f, upper %(dhi)f \n Approximate SD of ratio = %(appsd)f \
            #\n Approximate CV of ratio (%%) = %(cvr)f \n Approximate limits: lower %(applo)f, upper %(apphi)f' %flrd)
        else:
            self.txt.insert(END, "No calculation done, disc >= 0.")

if __name__ == "__main__":
    root=Tk()
    
    ff = FrameFieller(root)
    root.mainloop()
