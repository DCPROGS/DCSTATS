import sys
if sys.version_info[0] < 3:
    from Tkinter import *
    import tkSimpleDialog
else:
    from tkinter import *
    from tkinter import simpledialog as tkSimpleDialog

__author__="remis"
__date__ ="$27-May-2009 23:02:26$"

class DistPlotParam(tkSimpleDialog.Dialog):

    def body(self,master):

        self.title('Enter new plot parameters...')

        Label(master, text='Min X:').grid(row=0)
        Label(master, text='Max X:').grid(row=1)
        Label(master, text='Bin width:').grid(row=2)
        Label(master, text='Max Y').grid(row=3)

        self.e1 = Entry(master, justify=CENTER)
        self.e1.grid(row=0, column=1)
        self.e1.insert(END, '0')

        self.e2 = Entry(master, justify=CENTER)
        self.e2.grid(row=1, column=1)
        self.e2.insert(END, '10')

        self.e3 = Entry(master, justify=CENTER)
        self.e3.grid(row=2, column=1)
        self.e3.insert(END, '1')

        self.e4 = Entry(master, justify=CENTER)
        self.e4.grid(row=3, column=1)
        self.e4.insert(END, '1000')

        return self.e1 # initial focus

    def apply(self):
        self.xmin = int(self.e1.get())
        self.xmax = int(self.e2.get())
        self.dx = int(self.e3.get())
        self.ymax = int(self.e4.get())

