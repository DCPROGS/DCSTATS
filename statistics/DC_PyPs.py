#! /usr/bin/python

from Tkinter import *
from FrameFieller import FrameFieller
from FrameRantestContinuous import FrameRantestContinuous
from FrameRantestBinomial import FrameRantestBinomial


__author__="remis"
__date__ ="$30-Apr-2009 14:51:10$"

def on_fieller():
    FrameFieller()

def on_rantest_binomial():
    FrameRantestBinomial()

def on_rantest_continuous():
    FrameRantestContinuous()

def on_CVfit():
    pass

def on_help():
    pass

if __name__ == "__main__":

    # initiate main frame
    master = Tk() 
    master.title('DC statistics tools')    #   Main frame title
    master.geometry('300x200')
    menubar = Menu(master)

    statmenu = Menu(menubar,tearoff=0)

    statmenu.add_command(label="Fieller", command=on_fieller)

    statmenu.rantest = Menu(statmenu)
    statmenu.rantest.add_command(label="Continuously variable data", command=on_rantest_continuous)
    statmenu.rantest.add_command(label="Binomial data (each result= yes or no)", command=on_rantest_binomial)
    statmenu.add_cascade(label='Randomisation test', menu=statmenu.rantest)

    statmenu.add_command(label="CVfit", command=on_CVfit, state=DISABLED)
    statmenu.add_command(label="Help", command=on_help, state=DISABLED)
    statmenu.add_command(label="Quit!", command=master.quit)

    menubar.add_cascade(label="Statistical Tests", menu=statmenu)

    master.config(menu=menubar)
    message = Message(master, width = 450, text="Welcome to DC_PyPs! Please select a test to run.")
    message.pack()

    Label(master, text="").pack()
    picture = PhotoImage(file="dca2.gif")
    Label(master, image=picture).pack()
    
    master.mainloop()
