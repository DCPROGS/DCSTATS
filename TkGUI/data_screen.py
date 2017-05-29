# File: data_screen.py

__author__="remis"
__date__ ="$14-May-2009 12:23:09$"

import sys
import random
if sys.version_info[0] < 3:
    from Tkinter import *
    import tkSimpleDialog
else:
    from tkinter import *
    from tkinter import simpledialog as tkSimpleDialog

class Data_Screen(tkSimpleDialog.Dialog):

    def body(self,master):

        self.title('Enter data')

        Label(master, text="").grid(row=15, column=0, columnspan=2)
        Label(master, text="Sample 1").grid(row=16, column=0)
        Label(master, text="Sample 2").grid(row=16, column=2)
        Label(master, text="Number of measurements:").grid(row=17, column=0)
        Label(master, text="Number of measurements:").grid(row=17, column=2)
        Label(master, text="").grid(row=18, column=2)

        self.e1 = Entry(master, justify=CENTER)
        self.e1.grid(row=17, column=1)
        #self.e1.insert(END, '20')

        self.e2 = Entry(master, justify=CENTER)
        self.e2.grid(row=17, column=3)
        #self.e2.insert(END, '20')

        self.cols = []
        maxn = 20
        for i in range(2):
            rows = []
            for j in range(maxn):
                self.e = Entry(master, relief=RIDGE)
                self.e.grid(row=19+j, column=2*i, sticky=NSEW)
                #self.e.insert(END, '%d.%d' % (i, j))
                rows.append(self.e)

            self.cols.append(rows)

        return self.e1 # initial focus

    def apply(self):
        self.n1 = int(self.e1.get())
        self.n2 = int(self.e2.get())
        self.data = []

        for col in self.cols:
            for row in col:
                st = row.get()
                if st != '':
                    self.data.append(float(st))

