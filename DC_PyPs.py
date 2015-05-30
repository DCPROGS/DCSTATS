#! /usr/bin/python
from os import system
import sys
from platform import system as platform
from Tkinter import *
from FrameFieller import FrameFieller
from FrameRantestContinuous import FrameRantestContinuous
from FrameRantestBinomial import FrameRantestBinomial


__author__="remis"
__date__ ="$30-Apr-2009 14:51:10$"

class DCP:
    def __init__(self, master):
        frame = Frame(master)
        frame.config(background="#dcdcdc") #well, it has to be, right
        frame.pack()
        master.title('DC_PyPs v. 0.3')    #   Main frame title
        master.config(background="#dcdcdc")
        #master.geometry('450x480')
        menubar = Menu(master)
        
        statmenu = Menu(menubar,tearoff=0)
        
        statmenu.add_command(label="Fieller", command=self.on_fieller)
        
        statmenu.rantest = Menu(statmenu)
        statmenu.rantest.add_command(label="Continuously variable data", command=self.on_rantest_continuous)
        statmenu.rantest.add_command(label="Binomial data (each result= yes or no)", command=self.on_rantest_binomial)
        statmenu.add_cascade(label='Randomisation test', menu=statmenu.rantest)
        
        statmenu.add_command(label="CVfit", command=self.on_CVfit, state=DISABLED)
        statmenu.add_command(label="Help", command=self.on_help, state=DISABLED)
        statmenu.add_command(label="Quit", command=master.quit)
        
        menubar.add_cascade(label="Statistical Tests", menu=statmenu)
        
        master.config(menu=menubar)
        lframe = LabelFrame(master, width = 450, text="Welcome to DC statistics tools!", background="#dcdcdc")
        
        lframe.pack()
        
        Label(lframe, text="Please select a test to run:", background="#dcdcdc").pack()
        
        b2 = Button(lframe, text=" Randomisation test: Continuous data ", command=self.on_rantest_continuous, highlightbackground="#dcdcdc")
        b3 = Button(lframe, text="  Randomisation test: Binomial data  ", command=self.on_rantest_binomial, highlightbackground="#dcdcdc")
        b4 = Button(lframe, text=" Fieller's theorem for SD of a ratio ", command=self.on_fieller, highlightbackground="#dcdcdc")
        b2.pack()
        b3.pack()
        b4.pack()
        
        Label(lframe, text="", background="#dcdcdc").pack()
        picture = PhotoImage(file="dca2.gif")
        Label(lframe, image=picture).pack()
        Label(lframe, text="DC", background="#dcdcdc").pack()
        
        version = Message(lframe, width = 450, text="\n\nPython version: "+sys.version, background="#dcdcdc", font=("Helvetica", 12))
        version.pack()
        
        
        if platform() == 'Darwin':
            print ("Trying to force window to the front on Mac OSX")
            
            try:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            except:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python2.7" to true' ''')
        #finally:
        #print ("Failed")

    

    def on_fieller(self):
        ff = Toplevel(master)
        FrameFieller(ff)

    def on_rantest_binomial():
        FrameRantestBinomial()

    def on_rantest_continuous():
        FrameRantestContinuous()

    def on_CVfit():
        pass

    def on_help():
        pass

if __name__ == "__main__":

    print (sys.version) #parentheses necessary in python 3.
    # OSX Notes 6/12/14
    # ---------
    # usr/bin/python is 2.7.6 in Yosemite (10.10) and uses Tcl 8.5 (64-bit and thus can be retina).
    # This environment is used if DC_Pyps.py is launched from an Automator Script
    # DC_pyps does not need numpy etc so can use native Python from Apple
    # by contrast Tcl 8.4 is 32-bit and non-retina - used by 2.7.1 which is the default on AJRP's 2013 retina
    # macbook see
    # https://www.python.org/download/mac/tcltk/ for details
    # http://stackoverflow.com/questions/1405913/
    #
    
    # initiate main frame
    master = Tk()
    app = DCP(master)
    master.mainloop()






