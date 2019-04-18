#! /usr/bin/env python
"""
Launch rantest GUI: PyQt5 or Tk.
"""

import sys

if __name__ == "__main__":
    
    print (sys.version)
    try:
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import QApplication
        from GUI import QTdcstats
        app = QApplication(sys.argv)
        form = QTdcstats.DCStatsQT()
        form.show()
        app.exec_()
        
    except:
        if sys.version_info[0] < 3:
            from Tkinter import *
        else:
            from tkinter import *    
        from GUI.DC_Stats_Tk import *
        # initiate main frame
        master = Tk()
        app = DCP(master)
        master.mainloop()
    


    