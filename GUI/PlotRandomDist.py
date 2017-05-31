import random
import math
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *
    
from GUI.DistPlotParam import DistPlotParam

__author__="remis"
__date__ ="$24-May-2009 23:52:01$"

class PlotRandomDist(object):
    'Displays randomisation distribution.'

    def defineBin(self, binomial, xmin, xmax):
        'Defines bin width and number of bins. '

        # round down minimum value, so get Xmin for distribution
        # round up maximum value, so get Xmax for distribution
        xmin1 = int(xmin - 1)
        xmax1 = int(xmax + 1)

        nbin = 1
        if binomial:
            dx = 1    # bin width; 1 for binomial
            nbin = int(float(xmax1 - xmin1) / dx)
            while nbin > 20:
                dx = dx + 1
                nbin = int(float(xmax1 - xmin1) / dx)

        else:
            reduceXmin = 1
            while reduceXmin:
                xmin2 = xmin1 / 10.0
                if math.fabs(xmin) < math.fabs(xmin2):
                    xmin1 = xmin2
                else: reduceXmin = 0
            
            reduceXmax = 1
            while reduceXmax:
                xmax2 = xmax1 / 10.0
                if xmax < xmax2:
                    xmax1 = xmax2
                else: reduceXmax = 0
            nbin = 20
            dx = math.fabs(xmax1 - xmin1)/ nbin

        return xmin1, nbin, dx

    def createBins(self, xmin1, nbin, dx):
        'Create bins.'
        xaxis = []
        xaxis.append(xmin1)
        for j in range(0, nbin+1):
            xaxis.append(xmin1 + (j+1) * dx)
        return xaxis

    def sortRand(self, rand, xaxis):
        'Sorts rand data into bins.'

        nran = len(rand)
        nbin = len(xaxis) - 1

        # create frequency list
        freq = []
        for i in range(0, nbin):
            freq.append(0)

        # now sort
        for i in range(0, nran):
            ran = rand[i]
            for j in range(0, nbin):
                if ran >= xaxis[j] and ran < xaxis[j+1]:
                    freq[j] = freq[j] + 1

        # found maximal density value
        ymax = 0.0
        for j in range(0, nbin):
            if freq[j] > ymax: ymax = freq[j]
        ymax1 = int(ymax+0.5)    # max for plot

        return ymax1, freq

    def createFrame(self, xaxis, freq, ymax1, mean, xAxisTitle):
        'Crreates frame for plot'

        root = tk.Tk()
        root.title("Frequency distribution")
        root.resizable(width='FALSE', height='FALSE')    # should make window not resizable
        cwidth = 400
        cheight = 350
        c = tk.Canvas(root, width=cwidth, height=cheight, bg= 'white')
        c.grid(row=0, column=0, columnspan=2)

        xMinPix = int(cwidth * 15 / 100)
        xMaxPix = int(cwidth * 95 / 100)
        yMaxPix = int(cheight * 5 / 100)
        yMinPix = int(cheight * 85 / 100)

        # x Axis
        c.create_line(xMinPix,yMinPix,xMaxPix,yMinPix, width=2)    # axis
        c.create_line(xMinPix,yMinPix,xMinPix,yMinPix+5, width=2)    # tick
        c.create_text(xMinPix-5, yMinPix+10, text='%f'% (xaxis[0]))
        c.create_line(xMaxPix,yMinPix,xMaxPix,yMinPix+5, width=2)    # tick
        c.create_text(xMaxPix-5, yMinPix+10, text='%f'% (xaxis[-1]))
        c.create_text(int(xMaxPix/1.9), yMinPix+25, text=xAxisTitle, font=("Arial", "10", "bold"))


        # y Axis
        c.create_line(xMinPix,yMinPix,xMinPix,yMaxPix,  width=2)
        c.create_line(xMinPix,yMinPix,xMinPix-5,yMinPix, width=2)
        c.create_text(xMinPix-20, yMinPix-2, text='%d'% (0))
        c.create_line(xMinPix,yMaxPix,xMinPix-5,yMaxPix, width=2)
        c.create_text(xMinPix-20, yMaxPix-2, text='%d'% (ymax1))
        #c.create_text(230, 230, text="Frequency", fill="purple", font=("Helvectica", "16"))


        xMinDbl = float(xaxis[0])
        xMaxDbl = float(xaxis[-1])
        yMinDbl = float(0)
        yMaxDbl = float(ymax1)
        xScaleDbl = float(xMaxPix - xMinPix) / (xMaxDbl - xMinDbl)
        yScaleDbl = float(yMaxPix - yMinPix) / (yMaxDbl - yMinDbl)

        nbin = len(xaxis) - 1
        for i in range(0, nbin):
            x0 = xMinPix + int((float(xaxis[i])-xMinDbl) * xScaleDbl)
            x1 = xMinPix + int((float(xaxis[i+1])-xMinDbl) * xScaleDbl)
            y0 = yMinPix
            y1 = yMinPix + int(float(freq[i]) * yScaleDbl)
            # draw the bar
            c.create_rectangle(x0, y0, x1, y1, fill="red")
            # put the y value above each bar
            #c.create_text(x0+2, y1, anchor=tk.SW, text=str(self.freq[i]))

        # draw small triangle arrow at particular x
        xArrDbl = mean
        xArr = xMinPix + int((float(xArrDbl)-xMinDbl) * xScaleDbl)
        c.create_line(xArr, yMinPix, xArr-5, yMinPix+10, width=2, fill="blue")
        c.create_line(xArr, yMinPix, xArr+5, yMinPix+10, width=2, fill="blue")
        c.create_line(xArr+5, yMinPix+10, xArr-5, yMinPix+10, width=2, fill="blue")


        b1 = tk.Button(root, text="REPLOT", command=self.callback1) #, state=tk.DISABLED)
        b1.grid(row=1, column=0)
        b2 = tk.Button(root, text="Save ASCII", command=self.callback2, state=tk.DISABLED)
        b2.grid(row=1, column=1)

        self.root = root
        root.mainloop()

    def callback1(self):
        'Called by REPLOT button.'

        params = DistPlotParam(self.root)
        xmin1 = params.xmin
        xmax1 = params.xmax
        dx = params.dx
        ymax2 = params.ymax
        nbin = int((xmax1 - xmin1) / dx) - 1

        xaxis = self.createBins(xmin1, nbin, dx)
        ymax1, freq = self.sortRand(self.rand, xaxis)
        self.createFrame(xaxis, freq, ymax2, self.mean, self.xAxisTitle1)

    def callback2(self):
        'Called by Save ASCII button.'
        pass

    def __init__(self, rand, paired, binomial, icrit, mean):

        self.mean = mean
        plotType = 0
        if binomial: plotType = 1
        if not binomial: plotType = 2
        if paired: plotType = 3

        xAxisTitle = []
        xAxisTitle.append('Random numbers')
        xAxisTitle.append('Random number of successes in set')
        xAxisTitle.append('Random difference between means')
        xAxisTitle.append('Random mean of differences')
        self.xAxisTitle1 = xAxisTitle[plotType]

        self.rand = rand
        rmin = min(rand)
        rmax = max(rand)
        #min, max = self.getMinMax(rand)
        xmin1, nbin, dx = self.defineBin(binomial, rmin, rmax)
        xaxis = self.createBins(xmin1, nbin, dx)
        ymax1, freq = self.sortRand(rand, xaxis)
        self.createFrame(xaxis, freq, ymax1, self.mean, self.xAxisTitle1)
        

if __name__ == "__main__":
    randX = []
    sum = 0.0
    nran = 5000
    for i in range(nran):
        u = random.randint(0,10)
        randX.append(u)
        sum = sum + u
    mean = sum / float(nran)
    C = PlotRandomDist(randX, 0,1,1, mean);