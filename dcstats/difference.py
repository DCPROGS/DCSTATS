#!/usr/bin python
"""difference.py -- calculate statistics for a difference of two means."""

import math
import numpy as np
import matplotlib.pyplot as plt

import dcstats.statistics_EJ as s

__author__="remis"
__date__ ="$09-Apr-2019 13:48:16$"

class Difference:
    def __init__(self, S1, S2, r=0):
        """ 
        Calculate statistics of a difference of two means.

        Parameters
        ----------
        S1, S2 : ndarrays
            Observations in first and second trials.
        r : float
             Correlation coefficient.

        Attributes
        ----------
        A, B : ndarray
            Observations in first and second trials with wich
            Difference class is initialised. 
        r : float
            Correlation coefficient.
        df : integer
            Degree of freedom.
        difference : float
            Difference of means.
        meanA, meanB : floats
            Means of samples A and B.
        sdA, sdB : floats
            Standard deviations of samples A and B.
        sdmA, sdmB :floats
            Standard deviation of the mean of samples A and B.

        Methods
        -------
        SDM
        CIs
        bootstrap_difference
        run_bootstrap
        bootstrapped_CIs

        """   
        self.A, self.B = S1, S2
        self.r = r
        self.df = len(self.A) + len(self.B) - 2
        self.difference = np.mean(self.A) - np.mean(self.B)

        self.meanA, self.meanB = np.mean(self.A), np.mean(self.B)
        self.sdA, self.sdB = np.std(self.A, ddof=1), np.std(self.B, ddof=1) 
        self.sdmA = self.sdA / math.sqrt(len(self.A))
        self.sdmB = self.sdB / math.sqrt(len(self.B)) 

        self.__difference_is_bootstrapped = False
    
    def SDM(self):
        """ Calculate approximate standard deviation of the mean for the difference
            of two means.""" 
        var = self.sdmA + self.sdmB - self.r * self.sdmA * self.sdmB
        return math.sqrt(var)

    def CIs(self, alpha=0.05):
        """ Calculate approximate confidence intervals for the diffrence of two means. """
        tval = s.InverseStudentT(self.df, 1 - alpha / 2.0)
        lower = self.difference - tval * self.SDM()
        upper = self.difference + tval * self.SDM()
        return lower, upper

    def bootstrap_difference(self, A, B, runs=5000):
        """Bootstrap samples to get distribution for the difference of two means."""
        bdiffs = np.zeros(runs)
        for i in range(runs):
            a = np.mean(np.random.choice(A, size=len(A), replace=True))
            b = np.mean(np.random.choice(B, size=len(B), replace=True))
            bdiffs[i] = a - b
        bdiffs.sort()
        return bdiffs

    def run_bootstrap(self, runs=5000):
        """Bootstrap the difference of two means and calculate statistics 
        of bootstrapped distribution."""
        self.boot = self.bootstrap_difference(self.A, self.B, runs)
        self.bootstrap_mean = np.mean(self.boot)
        self.bootstrap_sdm = np.std(self.boot, ddof=1)
        self.bootstrap_runs = runs
        self.bootstrap_bias = self.difference - np.mean(self.boot)
        self.__difference_is_bootstrapped = True

    def bootstrapped_CIs(self, alpha=0.05):
        """Calculate confidence intervals for the bootstrapped difference."""
        lowerCI = self.boot[int((alpha / 2.0) * self.bootstrap_runs)]
        upperCI = self.boot[int((1 - alpha / 2.0) * self.bootstrap_runs)]
        return lowerCI, upperCI

    def plot_bootstrap(self, fig=None):
        """Plot bootstrapped distribution."""
        lower95CI, upper95CI = self.bootstrapped_CIs(alpha=0.05)
        if fig is None:
            fig, ax  = plt.subplots(1,1) #, figsize=(4,4))
        else: 
            fig.clf()
            ax = fig.add_subplot(1,1,1)
        ax.hist(self.boot, 20)
        ax.axvline(x=self.difference, color='r', label='observed difference')
        ax.axvline(x=self.bootstrap_mean, color='r', linestyle="dashed", 
                   label='bootstrapped difference')
        ax.axvline(x=lower95CI, color='k', linestyle="dashed", label='2.5% limits')
        ax.axvline(x=upper95CI, color='k', linestyle="dashed")
        ax.set_ylabel("Frequency")
        ax.set_xlabel('Diffrence (mean A - mean B)')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)
        plt.tight_layout()
        return fig

    def __repr__(self):
        lower95CI, upper95CI = self.CIs(alpha=0.05)
        repr_string = ('\nDifference = {0:.3g} +/- {1:.2g} (SDM)'.
            format(self.difference, self.SDM()) +
            '\n\t95% confidence limits:\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(lower95CI, upper95CI)
            )
        if self.__difference_is_bootstrapped:
            lower95CI, upper95CI = self.bootstrapped_CIs(alpha=0.05)
            repr_string += ('\n\nBootsrapping statistics (repeats = {0:d}):'.
            format(self.bootstrap_runs) +
            '\nDifference= {0:.3g} +/- {1:.2g} (bootstrapped SDM); bias= {2:.2g}'.
            format(self.difference, self.bootstrap_sdm, self.bootstrap_bias) +
            '\n\t95% confidence limits (bootstrapped):\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(lower95CI, upper95CI)
            )
        return repr_string

