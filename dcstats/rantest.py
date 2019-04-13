#!/usr/bin python
"""rantest.py -- RANDOMISATION TEST FOR TWO SAMPLES.\
               Converted from David Colquhoun's FORTRAN version RANTEST.FOR"""

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt

import dcstats.basic_stats as bs
from dcstats.hedges import Hedges_d

__author__="Remis Lape"
__date__ ="$01-May-2009 17:42:28$"

RTINTROD = "\nRANTEST: performs a randomisation test to compare two \
independent samples.\n\
According to the null hypothesis of no-difference, each outcome would \n\
have been the same regardless of which group the individual happened to\n\
be allocated. Therefore all N=n1+n2 observations are pooled and, as in\n \
the actual experiment, divided at random into groups of size n1 and n2.\n \
The fraction of randomisations that gives rise to a difference between\n \
the groups at least as large as that observed gives the P value.\n\
In the binomial case, in which the measurement is the fraction of 'successes'\n\
in each sample (say r1 out of n1, and r2 out of n2) a ''success'' is given\n\
a score of 1, ''failure'' = 0.\n"

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
        self.ir1, self.if1 = ir1, if1
        self.ir2, self.if2 = ir2, if2
        self.ir = ir1 + ir2
        self.n1 = ir1 + if1 # tot number of tests in first trial 
        self.n2 = ir2 + if2 # tot number of tests in second trial
        self.ntot = self.n1 + self.n2
        self.dobs = ir1 / float(self.n1) - ir2 / float(self.n2)
        random.seed(1984)
        
    def run_rantest(self, nran):
        self.nran = nran
        self.randiff = np.zeros(nran) # difference between means
        self.randis1 = np.zeros(nran) # number of success in randomised first trial
        allobs = [1]*self.ir + [0]*(self.ntot - self.ir)
        for k in range(0, self.nran):
            random.shuffle(allobs)
            is2 = sum(allobs[self.n1:])
            self.randiff[k] = (self.ir - is2) / float(self.n1) - is2 / float(self.n2)
            self.randis1[k] = self.ir - is2
        self.ng1 = self.randiff[self.randiff >= self.dobs].size
        self.ne1 = self.randiff[self.randiff == self.dobs].size
        self.nl1 = self.randiff[self.randiff <= self.dobs].size
        
    def __repr__(self):        
        return ('\n\n Rantest:  {0:d} randomisations:'.format(self.nran) +
            '\n P values for difference between sets are:' +
            '\n  r1 greater than or equal to observed: P = {0:.6f}'.format(self.ng1 / float(self.nran)) +
            '\n  r1 less than or equal to observed: P = {0:.6f}'.format(self.nl1 / float(self.nran)) +
            '\n  r1 equal to observed: number = {0:d} (P = {1:.6f})'.format(self.ne1, self.ne1 / float(self.nran)))


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

    def describe_data(self):
        """ Run Student's two-tailed t-test for a difference between two samples
        and calculate Hedges effect size. Return results as string. """
        ttc = bs.TTestContinuous(self.X, self.Y, self.are_paired)
        #calculation of hedges d and approximate 95% confidence intervals
        #not tested against known values yet AP 170518
        hedges_calculation = Hedges_d(self.X, self.Y)
        hedges_calculation.hedges_d_unbiased()
        #lowerCI, upperCI = hedges_calculation.approx_CI(self.paired)
        #paired needed for degrees of freedom
        hedges_calculation.bootstrap_CI(5000)
        #option to have bootstrap calculated CIs should go here
        return str(ttc) + str(hedges_calculation)

            
    def run_rantest(self, nran):
        """ Resample without replacement nran times and get statistics of obtained distribution. """
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
        self.nequal = self.randiff[np.fabs(self.randiff) == math.fabs(self.dbar)].size
        self.p2tail = self.n2tail / float(self.nran)
        self.pequal = self.nequal / float(self.nran)
        self.lo95lim = np.percentile(self.randiff, 2.5)
        self.hi95lim = np.percentile(self.randiff, 97.5)

    def plot_rantest(self, fig=None):
        """Plot randomisation distribution."""
        if fig is None:
            fig, ax  = plt.subplots(1,1) #, figsize=(4,4))
        else: 
            fig.clf()
            ax = fig.add_subplot(1,1,1)
        ax.hist(self.randiff, 20)
        ax.axvline(x=self.dbar, color='r', label='observed difference')
        ax.axvline(x=-self.dbar, color='r')
        ax.axvline(x=self.lo95lim, color='k', linestyle='--', label='2.5% limits')
        ax.axvline(x=self.hi95lim, color='k', linestyle='--')
        ax.set_xlabel('difference between means')
        ax.set_ylabel('frequency')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)
        plt.tight_layout()
        return fig
        
    def __repr__(self):
        return ('\nRantest:  {0:d} randomisations'.format(self.nran) +
        '\nTwo-tailed P = {0:.3e}'.format(self.p2tail) + 
        '\t(greater than or equal in absolute value to observed)' +
        '\nPequal = {0:.3e}'.format(self.pequal) +
        '\t(equal in absolute value to observed)')


class RantestBatch():
    def __init__(self, dataframe, log):
        """ 
        Parameters
        ----------
        dataframe : Pandas data frame containing multiple samples
        """   
        self.df = dataframe
        self.names = self.df.columns.tolist()
        self.n = len(self.names)
        self.log = log

    def run_rantest(self, nran):
        for i in range(self.n-1):
            for j in range(i+1, self.n):
                rnt = RantestContinuous(self.df.iloc[:, i].dropna().values.tolist(), 
                                        self.df.iloc[:, j].dropna().values.tolist())
                rnt.run_rantest(nran)
                self.log.append('\n*****   ' + self.names[i] + ' versus ' + 
                                self.names[j] + '   *****')
                self.log.append(rnt.describe_data())
                self.log.append(str(rnt))