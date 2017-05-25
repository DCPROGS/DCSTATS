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

class RantestBinomial(Rantest):
    
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
        
        self.__rantest_done = False
        self.__t_test()

    def __t_test(self):
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

    def run_rantest(self, nran):

        self.nran = nran
        self.dobs = self.p1 - self.p2
        allobs = [1]*self.ir1 + [0]*self.if1 + [1]*self.ir2 + [0]*self.if2

        self.randiff = []
        self.randis1 = []
        for n in range(0, self.nran):
            # this if is needed for Python backward compatibility 
            if sys.version_info[0] < 3: 
                iran = range(0,(self.n1 + self.n2))
            else:
                iran = list(range(0, self.n1 + self.n2))
            random.shuffle(iran)
            
            # number of success in randomised second trial
            is2 = [allobs[i] for i in iran[self.n1:]].count(1)
            is1 = self.ir1 + self.ir2 - is2 # number of success in randomised first trial
            dran = is1 / float(self.n1) - is2 / float(self.n2) # difference between means
            self.randis1.append(float(is1))
            self.randiff.append(float(dran))
            
        self.ng1 = len([i for i in self.randiff if i >= self.dobs])
        self.ne1 = len([i for i in self.randiff if i == self.dobs])
        self.nl1 = len([i for i in self.randiff if i <= self.dobs])

        self.pg1 = float(self.ng1) / float(self.nran)
        self.pl1 = float(self.nl1) / float(self.nran)
        self.pe1 = float(self.ne1) / float(self.nran)
        self.__rantest_done = True
        
    def __repr__(self):
        
        repr_string = ('\n Set 1: {0:d} successes out of {1:d};'.format(self.ir1, self.n1) +
            '\n p1 = {0:.6f};   SD(p1) = {1:.6f}'.format(self.p1, self.sd1) +
            '\n Set 2: {0:d} successes out of {1:d};'.format(self.ir2, self.n2) +
            '\n p2 = {0:.6f};   SD(p2) = {1:.6f}'.format(self.p2, self.sd2) +
            '\n Observed difference between sets, p1-p2 = {0:.6f}'.format(self.p1 - self.p2) +
            '\n\n Observed 2x2 table:' +
            '\n  Set 1:    {0:d}      {1:d}      {2:d}'.format(self.ir1, self.if1, self.n1) +
            '\n  Set 2:    {0:d}      {1:d}      {2:d}'.format(self.ir2, self.if2, self.n2) +
            '\n  Total:    {0:d}      {1:d}      {2:d}'.format(
            self.ir1 + self.ir2, self.if1 + self.if2, self.n1 + self.n2))
            
        if self.__rantest_done == True:
            repr_string += ('\n\n Two-sample unpaired test using Gaussian approximation to binomial:' +
                '\n standard normal deviate = {0:.6f}; two tail P = {1:.6f}.'.format(self.tval, self.P) +
                '\n\n {0:d} randomisations:'.format(self.nran) +
                '\n P values for difference between sets are:' +
                '\n  r1 greater than or equal to observed: P = {0:.6f}'.format(self.pg1) +
                '\n  r1 less than or equal to observed: P = {0:.6f}'.format(self.pl1) +
                '\n  r1 equal to observed: number = {0:d} (P = {1:.6f})'.format(self.ne1, self.pe1))
        return repr_string

class RantestContinuous(object):
    def __init__(self, X, Y, are_paired):
        """ 
        Parameters
        ----------
        X : observations in first trial, list of floats
        Y : observations in second trial, list of floats
        are_paired : are observations paired, boolean
        """
        
        self.X, self.Y = X, Y
        # calculate mean and variance of nx and ny
        self.xbar, self.sdx, self.sex = self.__meanvar(self.X)
        self.ybar, self.sdy, self.sey = self.__meanvar(self.Y)

        self.nx, self.ny = len(X), len(Y)
        self.D = []
        if are_paired and self.nx == self.ny:
            self.df = self.nx - 1
            self.are_paired = True
            for i in range(self.nx):
                self.D.append(self.X[i] - self.Y[i])    # differences for paired test
            self.dbar, self.sdd, self.sed = self.__meanvar(self.D)
            self.t_type = "Two-sample paired Student's t test"
        else:
            self.df = self.nx + self.ny - 2
            self.t_type = "Two-sample unpaired Student's t test"
            self.are_paired = False
            
        self.__rantest_done = False
        self.__t_test()
        
    def __meanvar(self, X):
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
        return xbar, sdx, sex

    def __t_test(self):
        if self.are_paired:               # And do a 2-sample paired t-test
            df = self.nx - 1
            self.sdbar = self.sdd / math.sqrt(self.ny)
            self.tval = self.dbar / self.sdbar
            x = self.df / (self.df + self.tval * self.tval)
            self.P = incompleteBeta(x, 0.5 * self.df, 0.5)
        else:    # if not paired
            s = (self.sdx * self.sdx * (self.nx-1) + self.sdy * self.sdy * (self.ny-1)) / self.df
            sdiff = math.sqrt(s * (1.0 / self.nx + 1.0 / self.ny))
            adiff = math.fabs(self.xbar - self.ybar)
            self.tval = adiff / sdiff
            x = self.df / (self.df + self.tval * self.tval)
            self.P = incompleteBeta(x, 0.5 * self.df, 0.5)

    def doRantestContinuous(self, nran):

        self.dobs = 0.0
        allobs = []
        self.randiff = []
        # for randomisation
        self.ng1 = 0
        self.nl1 = 0
        self.na1 = 0
        self.ne1 = 0
        self.ne2 = 0

        if self.are_paired:
            self.dobs = self.dbar    # observed mean difference
            # put absolute differences into allobs() for paired test
            for i in range(0, self.nx):
                allobs.append(math.fabs(self.D[i]))
            # start randomisation
            for n in range(0, nran):
                sd = 0.0
                for i in range(0, self.nx):
                    u = random.random()
                    if u < 0.5:
                        sd = sd - allobs[i]
                    else:
                        sd = sd + allobs[i]
                dran = sd / float(self.nx)    # mean difference
                self.randiff.append(dran)
                if dran >= self.dobs: self.ng1 += 1
                if dran <= self.dobs: self.nl1 += 1
                if math.fabs(dran) >= math.fabs(self.dobs): self.na1 += 1
                if dran == self.dobs: self.ne1 += 1
                if math.fabs(dran) == math.fabs(self.dobs): self.ne2 += 1
                # end of if(paired)

        else:    # if not paired
            self.dobs = self.xbar - self.ybar
            # Put all obs into one array for unpaired test
            k = 0
            stot = 0.0
            for i in range(0, self.nx):
                k = k + 1
                stot = stot + self.X[i]
                allobs.append(self.X[i])
            for i in range(0, self.ny):
                k = k + 1
                stot = stot + self.Y[i]
                allobs.append(self.Y[i])

            # start randomisation
            for n in range(0, nran):
                if sys.version_info[0] < 3:
                    iran = range(0,(self.nx + self.ny))
                else:
                    iran = list(range(0,(self.nx + self.ny)))
                random.shuffle(iran)
                sy = 0.0
                for i in range(0, self.ny):
                    j = self.nx + self.ny - i - 1
                    sy = sy + allobs[iran[j]]

                sx = stot - sy
                xb1 = sx / float(self.nx)    # mean
                yb1 = sy / float(self.ny)    # mean
                dran = xb1 - yb1

                self.randiff.append(dran)
                if dran >= self.dobs: self.ng1 += 1
                if dran <= self.dobs: self.nl1 += 1
                if math.fabs(dran) >= math.fabs(self.dobs): self.na1 += 1
                if dran == self.dobs: self.ne1 += 1
                if math.fabs(dran) == math.fabs(self.dobs): self.ne2 += 1

        self.pg1 = self.ng1 / float(nran)
        self.pl1 = self.nl1 / float(nran)
        self.pe1 = self.ne1 / float(nran)
        self.pa1 = self.na1 / float(nran)
        self.pe2 = self.ne2 / float(nran)
        self.nran = nran
        self.__rantest_done = True
        
    def __repr__(self):
        
        repr_string = ('n \t\t {0:d}      \t  {1:d}'.format(self.nx, self.ny) +
            '\nMean \t\t {0:.6f}    \t  {1:.6f}'.format(self.xbar, self.ybar) +
            '\nSD \t\t {0:.6f}     \t  {1:.6f}'.format(self.sdx, self.sdy) +
            '\nSDM \t\t {0:.6f}     \t  {1:.6f}'.format(self.sex, self.sey))
        
        if self.nx == self.ny and self.are_paired:
            repr_string += ('\n\n Mean difference (dbar) = \t {0:.6f}'.format(self.dbar) +
            '\n  s(d) = \t {0:.6f} \t s(dbar) = \t {1:.6f}'.format(self.sdd, self.sed) +
            '\n  t({0:d})= \t dbar / s(dbar) \t = \t {1:.6f}'.format(self.df, self.tval) +
            '\n  two tail P =\t {0:.6f}'.format(self.P))
            
        if self.__rantest_done:
            repr_string += ('\n\n'+self.t_type +
            '\n\n   {0:d} randomisations'.format(self.nran) +
            '\n P values for difference between means ' +
            '\n  greater than or equal to observed: P = \t {0:.6f}'.format(self.pg1) +
            '\n  less than or equal to observed: P = \t {0:.6f}'.format(self.pl1) +
            '\n  greater than or equal in absolute value to observed: P = \t {0:.6f}'.format(self.pa1) +
            '\n  Number equal to observed = {0:d} (P= {1:.6f})'.format(self.ne1, self.pe1) +
            '\n  Number equal in absolute value to observed = {0:d} (P= {1:.6f})'.format(self.ne2, self.pe2))
            
        return repr_string
        
#    print('\n\nEffect size' +
#        '\n  Hedges unbiased d = \t {0:.6f}'.format(rnt.hedges_d) +
#        '\n  approximate 95%% confidence intervals ' +
#        '\n  upper 95%% CI =\t {0:.6f}'.format(rnt.hedges_upperCI) +
#        '\n  lower 95%% CI =\t {0:.6f}'.format(rnt.hedges_lowerCI))


# 444 lines
