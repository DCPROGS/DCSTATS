#!/usr/bin python
"""ratio.py -- calculate statistics for a ratio of two means."""

import math
import numpy as np
import matplotlib.pyplot as plt

import dcstats.basic_stats as bs
import dcstats.statistics_EJ as s

__author__="remis"
__date__ ="$09-Apr-2019 13:48:16$"

class Ratio:
    def __init__(self, S1, S2, r=0):
        """ 
        Calculate statistics of a ratio of two means.

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
            Ratio class is initialised. 
        r : float
            Correlation coefficient.
        df : integer
            Degree of freedom.
        ratio : float
            Ratio of means.
        meanA, meanB : floats
            Means of samples A and B.
        sdA, sdB : floats
            Standard deviations of samples A and B.
        sdmA, sdmB :floats
            Standard deviation of the mean of samples A and B.

        Methods
        -------
        approximate_SDM
        approximate_CIs
        fieller_CIs
        bootstrap_ratio
        run_bootstrap
        bootstrapped_CIs

        """   
        self.A, self.B = S1, S2
        self.r = r
        self.df = len(self.A) + len(self.B) - 2
        self.ratio = np.mean(self.A) / np.mean(self.B)

        self.meanA, self.meanB = np.mean(self.A), np.mean(self.B)
        self.sdA, self.sdB = np.std(self.A, ddof=1), np.std(self.B, ddof=1) 
        self.sdmA = self.sdA / math.sqrt(len(self.A))
        self.sdmB = self.sdB / math.sqrt(len(self.B)) 

        self.__ratio_is_bootstrapped = False
    
    def approximate_SDM(self):
        """ Calculate approximate standard deviation of the mean for the ratio
            of two means.""" 
        var = ((self.meanA / self.meanB) * ((self.sdmA / self.meanA)**2 + 
            (self.sdmB / self.meanB)**2 - 
            2.0 * self.r * self.sdmA * self.sdmB / (self.meanA * self.meanB)))
        return math.sqrt(var)

    def approximate_CIs(self, alpha=0.05):
        """ Calculate approximate confidence intervals for the ratio of two means. """
        tval = s.InverseStudentT(self.df, 1 - alpha / 2.0)
        lower = self.ratio - tval * self.approximate_SDM()
        upper = self.ratio + tval * self.approximate_SDM()
        return lower, upper

    def fieller_CIs(self, alpha=0.05):
        """Calculate exact confidence intervals for the ratio of two means according to 
        Fiellers theorem."""
        vA, vB = self.sdmA**2, self.sdmB**2
        cov = self.r * self.sdmA * self.sdmB
        tval = s.InverseStudentT(self.df, 1 - alpha / 2.0)
        g = tval**2 * vB / self.meanB**2
        # Write disc in a way that does not appear to divide by vb so OK to use vb=0
        # disc=va - 2.0*ratio*cov + rat2*vb - g*(va-cov*cov/vb)
        disc = vA - 2.0 * self.ratio * cov + self.ratio**2 * vB - g * (vA - self.r**2 * vA)
        clower, cupper = 0.0, 0.0
        if disc >= 0:
            d = (tval / self.meanB) * math.sqrt(disc)
            # Write pre in a way that does not appear to divide by vb
            # (which actually cancels) so OK to use vb=0 (use g=tval*tval*vb/(b*b))
            #	pre=ratio - g*cov/vb
            pre = self.ratio - (tval**2 * cov) / self.meanB**2
            f = 1.0 / (1.0 - g)
            clower = f * (pre - d)
            cupper = f * (pre + d)
        return clower, cupper

    def bootstrap_ratio(self, A, B, runs=5000):
        """Bootstrap samples to get distribution for the ratio of two means."""
        bratios = np.zeros(runs)
        for i in range(runs):
            a = np.mean(np.random.choice(A, size=len(A), replace=True))
            b = np.mean(np.random.choice(B, size=len(B), replace=True))
            bratios[i] = a / b
        bratios.sort()
        return bratios

    def run_bootstrap(self, runs=5000):
        """Bootstrap the ratio of two means and calculate statistics 
        of bootstrapped distribution."""
        self.boot = self.bootstrap_ratio(self.A, self.B, runs)
        self.bootstrap_mean = np.mean(self.boot)
        self.bootstrap_sdm = np.std(self.boot, ddof=1)
        self.bootstrap_runs = runs
        self.bootstrap_bias = self.ratio - np.mean(self.boot)
        self.__ratio_is_bootstrapped = True

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
        ax.hist(self.boot, 20, density=True)
        
        xmin = self.bootstrap_mean - 4 * np.std(self.boot, ddof=1)
        xmax = self.bootstrap_mean + 4 * np.std(self.boot, ddof=1)
        increase = (xmax - xmin) / 100
        x = np.arange(xmin, xmax, increase)
        pdf = [bs._pdf(x1, self.bootstrap_mean, np.std(self.boot, ddof=1)) for x1 in x]
        ax.plot(x, pdf, 'k', label='normal pdf')

        ax.axvline(x=self.ratio, color='r', label='observed ratio')
        ax.axvline(x=self.bootstrap_mean, color='r', linestyle="dashed", 
                   label='bootstrapped ratio')
        ax.axvline(x=lower95CI, color='k', linestyle="dashed", label='2.5% limits')
        ax.axvline(x=upper95CI, color='k', linestyle="dashed")
        ax.set_ylabel("Frequency")
        ax.set_xlabel('Ratio (mean A / mean B)')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        borderaxespad=0.)
        plt.tight_layout()
        return fig

    def __repr__(self):
        aprox_lower95CI, aprox_upper95CI = self.approximate_CIs(alpha=0.05)
        fieller_lower95CI, fieller_upper95CI = self.fieller_CIs(alpha=0.05)
        repr_string = ('\nRatio = {0:.3g} +/- {1:.2g} (approximate SDM)'.
            format(self.ratio, self.approximate_SDM()) +
            '\n\tapproximate 95% confidence limits:\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(aprox_lower95CI, aprox_upper95CI) +
            '\n\tFieller 95% confidence limits:\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(fieller_lower95CI, fieller_upper95CI)
            )
        if self.__ratio_is_bootstrapped:
            lower95CI, upper95CI = self.bootstrapped_CIs(alpha=0.05)
            repr_string += ('\n\nBootsrapping statistics (repeats = {0:d}):'.
            format(self.bootstrap_runs) +
            '\nRatio= {0:.3g} +/- {1:.2g} (bootstrapped SDM); bias= {2:.2g}'.
            format(self.ratio, self.bootstrap_sdm, self.bootstrap_bias) +
            '\n\t95% confidence limits (bootstrapped):\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(lower95CI, upper95CI)
            )
        return repr_string

