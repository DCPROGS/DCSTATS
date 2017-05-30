#!/usr/bin python
"""rantest.py -- RANDOMISATION TEST FOR TWO SAMPLES.\
               Converted from David Colquhoun's FORTRAN version RANTEST.FOR"""

import sys
import math
import random

import dcstats.basic_stats as bs

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
        return ('\n\n {0:d} randomisations:'.format(self.nran) +
            '\n P values for difference between sets are:' +
            '\n  r1 greater than or equal to observed: P = {0:.6f}'.format(self.pg1) +
            '\n  r1 less than or equal to observed: P = {0:.6f}'.format(self.pl1) +
            '\n  r1 equal to observed: number = {0:d} (P = {1:.6f})'.format(self.ne1, self.pe1))


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
        self.are_paired = are_paired
        # calculate mean and variance of nx and ny
        self.xbar, self.sdx, self.sdmx = bs.mean(self.X), bs.sd(self.X), bs.sdm(self.X)
        self.ybar, self.sdy, self.sdmy = bs.mean(self.Y), bs.sd(self.Y), bs.sdm(self.Y)

        self.nx, self.ny = len(X), len(Y)
        self.D = []
        if self.are_paired and self.nx == self.ny:
            self.df = self.nx - 1
            for i in range(self.nx):
                self.D.append(self.X[i] - self.Y[i])    # differences for paired test
            self.dbar, self.sdd, self.sdmd = bs.mean(self.D), bs.sd(self.D), bs.sdm(self.D)
        else:
            self.df = self.nx + self.ny - 2
            
    def run_rantest(self, nran):

        self.randiff = []
        self.na1 = 0
        self.ne2 = 0
        if self.are_paired:
            for n in range(nran):
                sd = 0.0
                for i in range(0, self.nx):
                    u = random.random()
                    if u < 0.5:
                        sd -= self.D[i]
                    else:
                        sd += self.D[i]
                dran = sd / float(self.nx)    # mean difference
                self.randiff.append(dran)
                if math.fabs(dran) >= math.fabs(self.dbar): self.na1 += 1
                if math.fabs(dran) == math.fabs(self.dbar): self.ne2 += 1
                # end of if(paired)

        else:    # if not paired
            self.dbar = self.xbar - self.ybar
            allobs = self.X + self.Y
            stot = sum(self.X) + sum(self.Y)
            # start randomisation
            for n in range(0, nran):
                random.shuffle(allobs)
                sy = sum(allobs[self.nx : ])
                dran = (stot - sy) / float(self.nx) - sy / float(self.ny)
                self.randiff.append(dran)
                if math.fabs(dran) >= math.fabs(self.dbar): self.na1 += 1
                if math.fabs(dran) == math.fabs(self.dbar): self.ne2 += 1
                
        self.ng1 = len([i for i in self.randiff if i >= self.dbar])
        self.ne1 = len([i for i in self.randiff if i == self.dbar])
        self.nl1 = len([i for i in self.randiff if i <= self.dbar])
        self.pg1 = self.ng1 / float(nran)
        self.pl1 = self.nl1 / float(nran)
        self.pe1 = self.ne1 / float(nran)
        self.pa1 = self.na1 / float(nran)
        self.pe2 = self.ne2 / float(nran)
        self.nran = nran
        
    def __repr__(self):
        return ('\n\n   Rantest:  {0:d} randomisations'.format(self.nran) +
        '\n P values for difference between means ' +
        '\n  greater than or equal to observed: P = \t {0:.6f}'.format(self.pg1) +
        '\n  less than or equal to observed: P = \t {0:.6f}'.format(self.pl1) +
        '\n  greater than or equal in absolute value to observed: P = \t {0:.6f}'.format(self.pa1) +
        '\n  Number equal to observed = {0:d} (P= {1:.6f})'.format(self.ne1, self.pe1) +
        '\n  Number equal in absolute value to observed = {0:d} (P= {1:.6f})'.format(self.ne2, self.pe2))

