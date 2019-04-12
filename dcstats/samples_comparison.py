import sys
import math
import random
import numpy as np

import dcstats.basic_stats as bs
from dcstats.hedges import Hedges_d

class TwoSamplesComparison:
    def __init__(self, S1, S2, are_paired=False):
        """ 
        Parameters
        ----------
        S1 : observations in first trial, list of floats
        S2 : observations in second trial, list of floats
        are_paired : are observations paired, boolean
        """   
        self.A, self.B = S1, S2
        self.nA, self.nB = len(self.A), len(self.B)
        self.are_paired = are_paired
        self.repr_string = ''
        
    def describe(self):
        """ Run Student's two-tailed t-test for a difference between two samples
        and calculate Hedges effect size. Return results as string. """
        ttc = bs.TTestContinuous(self.A, self.B, self.are_paired)
        #calculation of hedges d and approximate 95% confidence intervals
        #not tested against known values yet AP 170518
        hedges_calculation = Hedges_d(self.A, self.B)
        hedges_calculation.hedges_d_unbiased()
        #lowerCI, upperCI = hedges_calculation.approx_CI(self.paired)
        #paired needed for degrees of freedom
        hedges_calculation.bootstrap_CI(5000)
        #option to have bootstrap calculated CIs should go here
        return str(ttc) + str(hedges_calculation)

    def __repr__(self):
        self.repr_string = ('n \t\t {0:d}     \t{1:d}'.format(len(self.A), len(self.B)) +
            '\nMean \t\t {0:.6f}    \t  {1:.6f}'.format(np.mean(self.A), np.mean(self.B)) +
            '\nSD \t\t {0:.6f}     \t  {1:.6f}'.format(np.std(self.A), np.std(self.B)))
        return self.repr_string