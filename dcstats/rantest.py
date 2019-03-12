#!/usr/bin python
"""rantest.py -- RANDOMISATION TEST FOR TWO SAMPLES.\
               Converted from David Colquhoun's FORTRAN version RANTEST.FOR"""

import sys
import math
import random
import numpy as np

import dcstats.basic_stats as bs

# AP 091202 Minor corrections to spelling and spacing of introd.
# AP 140418 more cosmetic changes for deposition
# AP 150512 corrected implementation of paired tests, more verbose output.

__author__="Remis Lape"
__date__ ="$01-May-2009 17:42:28$"

RTINTROD = '\nRANTEST: performs a randomisation test to compare two \
independent samples. According to the null hypothesis\n \
of no-difference, each outcome would have been the same \
regardless of which group the individual happened to\n \
be allocated. Therefore all N=n1+n2 observations are \
pooled and, as in the actual experiment, divided at random\n \
into groups of size n1 and n2. The fraction \
of randomisations that gives rise to a difference between the groups\n \
at least as large as that observed \
gives the P value.\
\n In the binomial case, in which the measurement is the \
fraction of ''successes'' in each sample (say r1 out of n1, and\n \
r2 out of n2) a ''success'' is given a \
score of 1, ''failure'' = 0.\n'

RTCRITERION = " Randomisation test on binomial data could be done\
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


class RantestBinomial():
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
        return ('\n\n Rantest:  {0:d} randomisations:'.format(self.nran) +
            '\n P values for difference between sets are:' +
            '\n  r1 greater than or equal to observed: P = {0:.6f}'.format(self.pg1) +
            '\n  r1 less than or equal to observed: P = {0:.6f}'.format(self.pl1) +
            '\n  r1 equal to observed: number = {0:d} (P = {1:.6f})'.format(self.ne1, self.pe1))


class RantestContinuous():
    def __init__(self, X, Y, are_paired=False):
        """ 
        Parameters
        ----------
        X : observations in first trial, list of floats
        Y : observations in second trial, list of floats
        are_paired : are observations paired, boolean
        """   
        self.X, self.Y = X, Y
        self.nx, self.ny = len(X), len(Y)
        self.are_paired = are_paired
        random.seed(1984)
        np.random.seed(1984)
            
    def run_rantest(self, nran):
        self.nran = nran
        self.randiff = np.zeros(nran)
        if self.are_paired:
            self.D = np.array(self.X) - np.array(self.Y)
            self.dbar = np.mean(self.D)
            for i in range(nran):
                ones = np.ones(self.nx)
                ones[np.random.random(self.nx) < 0.5] *= -1             
                self.randiff[i] = np.sum(self.D * ones) / float(self.nx) # mean difference
        else:    # if not paired
            self.dbar = np.mean(self.X) - np.mean(self.Y)
            allobs = np.concatenate([self.X, self.Y])
            for i in range(0, nran):
                random.shuffle(allobs)
                sy = sum(allobs[self.nx : ])
                self.randiff[i] = (sum(allobs) - sy) / float(self.nx) - sy / float(self.ny)
        self.n2tail = self.randiff[np.fabs(self.randiff) >= math.fabs(self.dbar)].size
        self.p2tail = self.n2tail / float(self.nran)
        
    def __repr__(self):
        return ('\nRantest:  {0:d} randomisations'.format(self.nran) +
        '\nTwo-tailed P = {0:.3e}'.format(self.p2tail) + 
        '\t(greater than or equal in absolute value to observed)')