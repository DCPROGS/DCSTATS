#!/usr/bin python
"""twosamples.py -- calculate statistics of bootstrapped samples."""

import math
import numpy as np
import matplotlib.pyplot as plt

import dcstats.statistics_EJ as s
import dcstats.basic_stats as bs
from dcstats.hedges import Hedges_d

__author__="remis"
__date__ ="$14-Apr-2019 14:04:05$"

class TwoSamples:
    def __init__(self, df2, are_paired=False, r=0, runs=10000):
        """ 
        Bootstrap samples and calculate statistics.

        Parameters
        ----------
        df2 : pandas DataFrame
            Observations in first and second trials.
        r : float
             Correlation coefficient.

        Attributes
        ----------
        A, B : type ndarray
            Observations in first and second trials with wich
            Ratio class is initialised. 
        r : float
            Correlation coefficient.
        df : integer
            Degree of freedom.
        meanA, meanB : floats
            Means of samples A and B.
        sdA, sdB : floats
            Standard deviations of samples A and B.
        sdmA, sdmB :floats
            Standard deviation of the mean of samples A and B.

        Methods
        -------
        """   
        self.df2 = df2
        self.A = self.df2.iloc[:, 0].dropna().values.tolist()
        self.B = self.df2.iloc[:, 1].dropna().values.tolist()
        self.r = r
        self.are_paired = are_paired
        self.runs = runs

    def describe_data(self):
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

    def plot_bootstrapped_distributions(self, fig=None):
        sample1 = Sample(self.A)
        sample1.run_bootstrap(self.runs)
        lower95CI1, upper95CI1 = sample1.bootstrapped_CIs(alpha=0.05)
        
        sample2 = Sample(self.B)
        sample2.run_bootstrap(self.runs)
        lower95CI2, upper95CI2 = sample2.bootstrapped_CIs(alpha=0.05)
        
        if fig is None:
            fig = plt.Figure()
        else: 
            fig.clf()
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.hist(sample1.boot, bins=20)
        ax1.axvline(x=sample1.meanA, color='k', label='observed mean')
        ax1.axvline(x=sample1.bootstrap_mean, color='k', linestyle="dashed", 
                   label='bootstrapped mean')
        ax1.axvline(x=lower95CI1, color='r', linestyle="dashed", label='2.5% limits')
        ax1.axvline(x=upper95CI1, color='r', linestyle="dashed")
        ax1.set_ylabel("Frequency")
        ax1.set_xlabel('Mean')
        ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)

        ax2 = fig.add_subplot(1, 2, 2)
        ax2.hist(sample2.boot, bins=20)
        ax2.axvline(x=sample2.meanA, color='k', label='observed mean')
        ax2.axvline(x=sample2.bootstrap_mean, color='k', linestyle="dashed", 
                   label='bootstrapped mean')
        ax2.axvline(x=lower95CI2, color='r', linestyle="dashed", label='2.5% limits')
        ax2.axvline(x=upper95CI2, color='r', linestyle="dashed")
        ax2.set_ylabel("Frequency")
        ax2.set_xlabel('Mean')
        ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)

        plt.tight_layout()
        return fig

    def plot_qq_plots(self, fig=None):

        sample1 = Sample(self.A)
        q11, q12, min1, max1 = sample1.get_qq()
        sample2 = Sample(self.B)
        q21, q22, min2, max2 = sample2.get_qq()
        
        if fig is None:
            fig = plt.Figure()
        else: 
            fig.clf()
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.plot(q11, q12, 'o')
        ax1.plot([min1, max1],[min1, max1],'k--')
        ax1.set_ylabel('Normal sample quantiles')
        ax1.set_xlabel('Normal theoretical quantiles')

        ax2 = fig.add_subplot(1, 2, 2)
        ax2.plot(q21, q22, 'o')
        ax2.plot([min2, max2],[min2, max2],'k--')
        ax2.set_ylabel('Normal sample quantiles')
        ax2.set_xlabel('Normal theoretical quantiles')

        plt.tight_layout()
        return fig

    def plot_boxplot(self, fig=None):
        if fig is None:
            fig, ax  = plt.subplots(1,1) #, figsize=(4,4))
        else: 
            fig.clf()
            ax = fig.add_subplot(1,1,1)
        ax = self.df2.boxplot()
        for i in range(self.df2.shape[1]):
            X = self.df2.iloc[:, i].dropna().values.tolist()
            x = np.random.normal(i+1, 0.04, size=len(X))
            ax.plot(x, X, '.', alpha=0.4)
        plt.tight_layout()
        return fig


class Sample:
    def __init__(self, S):
        """ 
        Calculate statistics of a single sample.

        Parameters
        ----------
        S : ndarray
            Observations.

        Attributes
        ----------
        A : ndarray
            Sample of observations with wich class is initialised. 
        meanA : float
            Mean of sample A.
        sdA : float
            Standard deviations of sample A.
        sdmA :float
            Standard deviation of the mean of sample A.

        Methods
        -------
        SDM
        CIs
        bootstrap_sample
        run_bootstrap
        bootstrapped_CIs

        """   
        self.A = S
        self.nA = len(self.A)
        self.meanA = np.mean(self.A)
        self.sdA = np.std(self.A, ddof=1)
        self.sdmA = self.sdA / math.sqrt(len(self.A))
        self.__sample_is_bootstrapped = False

    def bootstrap_sample(self, A, runs=10000):
        """Bootstrap sample to get distribution of mean."""
        bmeans = np.zeros(runs)
        for i in range(runs):
            bmeans[i] = np.mean(np.random.choice(A, size=len(A), replace=True))
        bmeans.sort()
        return bmeans

    def run_bootstrap(self, runs=10000):
        """Bootstrap the sample and calculate statistics 
        of bootstrapped distribution."""
        self.boot = self.bootstrap_sample(self.A, runs)
        self.bootstrap_mean = np.mean(self.boot)
        self.bootstrap_sdm = np.std(self.boot, ddof=1)
        self.bootstrap_runs = runs
        self.bootstrap_bias = self.meanA - np.mean(self.boot)
        self.__sample_is_bootstrapped = True

    def bootstrapped_CIs(self, alpha=0.05):
        """Calculate confidence intervals for the bootstrapped ratios."""
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
        ax.axvline(x=self.meanA, color='k', label='observed ratio')
        ax.axvline(x=self.bootstrap_mean, color='k', linestyle="dashed", 
                   label='bootstrapped sample mean')
        ax.axvline(x=lower95CI, color='r', linestyle="dashed", label='2.5% limits')
        ax.axvline(x=upper95CI, color='r', linestyle="dashed")
        ax.set_ylabel("Frequency")
        ax.set_xlabel('Bootstrapped sample mean')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)
        plt.tight_layout()
        return fig

    def get_qq(self):
        # Sample to test for normality
        self.A.sort()
        quantile_levels1 = np.arange(self.nA, dtype=float) / self.nA
        quantiles1 = self.A

        #Calculate quantiles by generating samples from hypothetical normal distribution
        nSN = 1000
        SN = np.random.normal(self.meanA, self.sdA, nSN)
        SN.sort()
        quantile_levels2 = np.arange(nSN, dtype=float) / nSN
        quantiles2 = np.interp(quantile_levels1, quantile_levels2, SN)

        maxval = max(self.A[-1], SN[-1])
        minval = min(self.A[0], SN[0])
        return quantiles2, quantiles1, minval, maxval

    def __repr__(self):
        if self.__sample_is_bootstrapped:
            lower95CI, upper95CI = self.bootstrapped_CIs(alpha=0.05)
            repr_string += ('\n\nBootsrapped sample statistics (repeats = {0:d}):'.
            format(self.bootstrap_runs) +
            '\nMean= {0:.3g} +/- {1:.2g} (bootstrapped SDM); bias= {2:.2g}'.
            format(self.meanA, self.bootstrap_sdm, self.bootstrap_bias) +
            '\n\t95% confidence limits (bootstrapped):\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(lower95CI, upper95CI)
            )
        return repr_string


