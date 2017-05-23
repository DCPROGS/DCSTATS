#!/usr/bin python
"""rantest.py -- RANDOMISATION TEST FOR TWO SAMPLES.\
               Converted from David Colquhoun's FORTRAN version RANTEST.FOR"""

import sys
import math
import random

from statistics_EJ import incompleteBeta

# AP 091202 Minor corrections to spelling and spacing of introd.
# AP 140418 more cosmetic changes for deposition
# AP 150512 corrected implementation of paired tests, more verbose output.

__author__="Remis Lape"
__date__ ="$01-May-2009 17:42:28$"

class Rantest(object):

    introd = "  RANTEST performs a randomisation test to compare two " +\
    "independent samples.  According to the null hypothesis of " +\
    "no-difference, each outcome would have been the same " +\
    "regardless of which group the individual happened to " +\
    "be allocated to.  Therefore all N = n1 + n2 observations are " +\
    "pooled and, as in the actual experiment, divided at " +\
    "random into groups of size n1 and n2.  The fraction " +\
    "of randomisations that gives rise to a difference " +\
    "between the groups at least as large as that observed " +\
    "gives the P value.\n" +\
    "  In the binomial case, in which the measurement is the " +\
    "fraction of 'successes' in each sample (say r1 out " +\
    "of n1, and r2 out of n2) a 'success' is given a " +\
    "score of 1, 'failure' scores 0.\n"

    criterion =  " Randomisation test on binomial data could be done\
    using as criterion: (1) number of successes in set 1 (r1)\
    or (2) difference between the p=r/n values.\
    Both criteria give the same one-tail P value.\
    Use of r1 as criterion is the direct Monte Carlo\
    equivalent of summing the the exact Fisher test probabilities\
    for the observed 2x2 table with those for all tables that depart\
    further from the null hypothesis in the observed direction.\
    A 2-tail probablilty can be found by doubling the one-tail\
    value, at least if the displayed distribution is symmetrical\
    Use of (p1-p2) as criterion gives both one and two-tail\
    probabilities directly by seeing how many random allocations\
    of the observations to groups of size n1 and n2 produce and\
    absolute value of (p1-p2) at least as big as that observed."

    def __init__(self):
        pass

class RantestBinomial(object):
    
    def __init__(self, ir1, if1, ir2, if2):
        """ 
        Parameters
        ----------
        ir1 : number of successes in first trial, int
        if1 : number of failures in first trial, int
        ir2 : number of successes in second trial, int
        if2 : number of failures in second trial, int       
        """
        self.ir1 = ir1
        self.if1 = if1
        self.ir2 = ir2
        self.if2 = if2
        self.n1 = ir1 + if1 # tot number of tests in first trial 
        self.n2 = ir2 + if2 # tot number of tests in second trial
        self.p1 = float(self.ir1) / float(self.n1) # prob of success in first trial
        self.p2 = float(self.ir2) / float(self.n2) # prob of success in second trial

    def tTestBinomial(self):
        """" Use Gaussian approx to do 2 sample t test. """

        ppool = float(self.ir1 + self.ir2) / float(self.n1 + self.n2)
        self.sd1 = math.sqrt(self.p1 * (1.0 - self.p1) / float(self.n1))
        self.sd2 = math.sqrt(self.p2 * (1.0 - self.p2) / float(self.n2))
        sd1p = math.sqrt(ppool * (1.0 - ppool) / float(self.n1))
        sd2p = math.sqrt(ppool * (1.0 - ppool) / float(self.n2))
        sdiff = math.sqrt(sd1p * sd1p + sd2p * sd2p)

        self.tval = math.fabs(self.p1 - self.p2) / sdiff
        df = 100000    # to get Gaussian
        x = df / (df + self.tval **2)
        self.P = incompleteBeta(x, 0.5 *df, 0.5)

    def doRantestBinomial(self, icrit, nran):
        self.nran = nran

        self.dobs = self.p1 - self.p2
        allobs = []
        for i in range(0, self.n1):
            if i < self.ir1:
                allobs.append(1.0)
            else:
                allobs.append(0.0)
        for i in range(0, self.n2):
            if i < self.ir2:
                allobs.append(1.0)
            else:
                allobs.append(0.0)

        self.ng1 = 0
        self.nl1 = 0
        self.na1 = 0
        self.ne1 = 0
        self.ne2 = 0

        self.randiff = []

        for n in range(0, self.nran):

            # Randomisation happens here
            if sys.version_info[0] < 3:
                iran = range(0,(self.n1 + self.n2))
            else:
                iran = list(range(0, self.n1 + self.n2))
            random.shuffle(iran)

            is2 = 0.0
            for i in range(0, self.n2):
                j = self.n1 + self.n2 - i - 1
                is2 = is2 + allobs[iran[j]]
            is1 = self.ir1 + self.ir2 - is2
            xb1 = is1 / float(self.n1)    # mean
            yb1 = is2 / float(self.n2)    # mean
            dran = xb1 - yb1
            self.randiff.append(float(is1))

            # icrit=2
            if dran >= self.dobs: self.ng1 = self.ng1 + 1
            if dran <= self.dobs: self.nl1 = self.nl1 + 1
            if dran == self.dobs: self.ne1 = self.ne1 + 1
            if math.fabs(dran) >= math.fabs(self.dobs): self.na1 = self.na1 + 1
            if math.fabs(dran) == math.fabs(self.dobs): self.ne2 = self.ne2 + 1

        self.pg1 = float(self.ng1) / float(self.nran)
        self.pl1 = float(self.nl1) / float(self.nran)
        self.pe1 = float(self.ne1) / float(self.nran)
        self.pa1 = float(self.na1) / float(self.nran)
        self.pe2 = float(self.ne2) / float(self.nran)


class RantestContinuous(object):
    def __init__(self):
        self.dict = {}

    def meanvar(self, X):
        n = len(X)
        sumx = X[0]
        sumxx = 0.0
        for i in range(1, n):
            sumx = sumx + X[i]
            sumxx = sumxx + ((i+1) * X[i] - sumx)**2 / float((i+1)*i)
        xbar = sumx / float(n)
        varx = sumxx /float(n - 1)
        sdx = math.sqrt(varx)
        sex = sdx / math.sqrt(n)
        return xbar, varx, sdx, sex

    def tTestContinuous(self, xobs, yobs, paired):

        nx = len(xobs)
        ny = len(yobs)
        df = 1
        
        # calculate mean and variance of nx and ny
        xbar, varx, sdx, sex = self.meanvar(xobs)
        ybar, vary, sdy, sey = self.meanvar(yobs)
        
        D = []
        dbar = 0.0
        vard = 0.0
        sdd = 0.0
        sed = 0.0
        adiff = 0.0
        sdiff = 0.0
        sdbar = 0.0

        if paired and nx == ny:
            for i in range(0, nx):
                D.append(xobs[i] - yobs[i])    # differences for paired test
            dbar, vard, sdd, sed = self.meanvar(D)
            self.dict['tPaired'] = "Two-sample paired Student's t test"
                
        elif paired and nx != ny:
            print ("Paired test is impossible if nx != ny")
            paired = False
            self.dict['tPaired'] = "Paired tickbox check but paired tests impossible, nx != ny.\n Two-sample unpaired Student's t test."
        
        else:
            self.dict['tPaired'] = "Two-sample unpaired Student's t test"
        
       
        if paired:               # And do a 2-sample paired t-test
            
            df = nx - 1
            sdbar = sdd / math.sqrt(ny)
            tval = dbar / sdbar
            x = df / (df + tval * tval)
            #P = self.betai(0.5 * df, 0.5, x)
            P = incompleteBeta(x, 0.5 *df, 0.5)
   
        else:    # if not paired
            df = nx + ny - 2
            s = (sdx * sdx * (nx-1) + sdy * sdy * (ny-1)) / df
            sdiff = math.sqrt(s * (1.0 / nx + 1.0 / ny))
            adiff = math.fabs(xbar - ybar)
            tval = adiff / sdiff
            x = df / (df + tval * tval)
            #P = self.betai(0.5 * df, 0.5, x)
            P = incompleteBeta(x, 0.5 *df, 0.5)

        self.dict['xbar'] = xbar
        self.dict['varx'] = varx
        self.dict['sdx'] = sdx
        self.dict['sex'] = sex
        self.dict['ybar'] = ybar
        self.dict['vary'] = vary
        self.dict['sdy'] = sdy
        self.dict['sey'] = sey
        self.dict['dbar'] = dbar
        self.dict['vard'] = vard
        self.dict['sdd'] = sdd
        self.dict['sed'] = sed
        self.dict['P'] = P
        self.dict['tval'] = tval
        self.dict['df'] = df
        self.dict['adiff'] = adiff
        self.dict['sdiff'] = sdiff
        self.dict['sdbar'] = sdbar

    def setContinuousData(self, in_data, nran, jset, paired):
        
        #jset is a flag for larger datasets and compatibility with older programs?
        #normally called with 1
        #TODO set default jset value here?
        
        j_offset = (jset-1) * 7
        
        self.dict['nx'] = in_data[j_offset + 1]
        self.dict['ny'] = in_data[j_offset + 2]

        # AP 170517 are these global variables? they don't seem to be used elsewhere
        titled = in_data[j_offset + 3]
        titlex = in_data[j_offset + 4]
        titley = in_data[j_offset + 5]
        
        xobs = in_data[j_offset + 6]
        yobs = in_data[j_offset + 7]

        return xobs, yobs

    def doRantestContinuous(self, xobs, yobs, paired, nran):

        nx = len(xobs)
        ny = len(yobs)

        D = []
        if paired and nx == ny:
            for i in range(0, nx):
                D.append(xobs[i] - yobs[i])    # differences for paired test
            self.dict['RanPaired'] = "Paired randomisation test."
    
        elif paired and nx != ny:
            print ("Paired test is still impossible if nx != ny")
            paired = False
            self.dict['RanPaired'] = "Paired tickbox check but paired tests impossible, nx != ny.\n Doing unpaired randomisation test."
        
        else:
            self.dict['RanPaired'] = "Unpaired randomisation test."

        dobs = 0.0
        allobs = []
        randiff = []
        # for randomisation
        ng1 = 0
        nl1 = 0
        na1 = 0
        ne1 = 0
        ne2 = 0

        if paired:
            dobs = self.dict['dbar']    # observed mean difference
            # put absolute differences into allobs() for paired test
            for i in range(0, nx):
                allobs.append(math.fabs(D[i]))
            # start randomisation
            for n in range(0, nran):
                sd = 0.0
                for i in range(0, nx):
                    u = random.random()
                    if u < 0.5:
                        sd = sd - allobs[i]
                    else:
                        sd = sd + allobs[i]
                dran = sd / float(nx)    # mean difference
                randiff.append(dran)
                if dran >= dobs: ng1 = ng1 + 1
                if dran <= dobs: nl1 = nl1 + 1
                if math.fabs(dran) >= math.fabs(dobs): na1 = na1 + 1
                if dran == dobs: ne1 = ne1 + 1
                if math.fabs(dran) == math.fabs(dobs): ne2 = ne2 + 1
                # end of if(paired)

        else:    # if not paired

            dobs = self.dict['xbar'] - self.dict['ybar']
            # Put all obs into one array for unpaired test
            k = 0
            stot = 0.0
            for i in range(0, nx):
                k = k + 1
                stot = stot + xobs[i]
                allobs.append(xobs[i])
            for i in range(0, ny):
                k = k + 1
                stot = stot + yobs[i]
                allobs.append(yobs[i])

            # start randomisation
            for n in range(0, nran):
                if sys.version_info[0] < 3:
                    iran = range(0,(nx + ny))
                else:
                    iran = list(range(0,(nx + ny)))
                random.shuffle(iran)
                sy = 0.0
                for i in range(0, ny):
                    j = nx + ny - i - 1
                    sy = sy + allobs[iran[j]]

                sx = stot - sy
                xb1 = sx / float(nx)    # mean
                yb1 = sy / float(ny)    # mean
                dran = xb1 - yb1

                randiff.append(dran)
                if dran >= dobs: ng1 = ng1 + 1
                if dran <= dobs: nl1 = nl1 + 1
                if math.fabs(dran) >= math.fabs(dobs): na1 = na1 + 1
                if dran == dobs: ne1 = ne1 + 1
                if math.fabs(dran) == math.fabs(dobs): ne2 = ne2 + 1

        #store results for output
        self.dict['nran'] = nran
        self.dict['dobs'] = dobs
        self.dict['randiff'] = randiff

        self.dict['pg1'] = ng1 / float(nran)
        self.dict['pl1'] = nl1 / float(nran)
        self.dict['pe1'] = ne1 / float(nran)
        self.dict['pa1'] = na1 / float(nran)
        self.dict['pe2'] = ne2 / float(nran)
        self.dict['ng1'] = ng1
        self.dict['nl1'] = nl1
        self.dict['na1'] = na1
        self.dict['ne1'] = ne1
        self.dict['ne2'] = ne2

# 444 lines
