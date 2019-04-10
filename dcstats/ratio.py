#!/usr/bin python
"""ratio.py -- calculate statistics for a ratio of two means."""

import math
import numpy as np

import dcstats.statistics_EJ as s

__author__="remis"
__date__ ="$09-Apr-2019 13:48:16$"

class Ratio:
    def __init__(self, S1, S2):
        """ 
        Parameters
        ----------
        S1 : observations in first trial, numpy array or list
        S2 : observations in second trial, numpy array or list
        """   
        self.A = S1
        self.B = S2
        self.__ratio_is_bootstrapped = False
     
    def ratio(self):
        return np.mean(self.A) / np.mean(self.B)

    def ratio_approxSDM(self):
        return self.approximate_SDM(self.A, self.B)

    def ratio_approxCIs(self, alpha=0.05):
        return self.approximate_CIs(self.A, self.B, alpha)

    def reciprocal(self):
        return np.mean(self.B) / np.mean(self.A)

    def reciprocal_approxSDM(self):
        return self.approximate_SDM(self.B, self.A)

    def reciprocal_approxCIs(self, alpha=0.05):
        return self.approximate_CIs(self.B, self.A, alpha)

    def approximate_SDM(self, A, B, r=0.0):
        mA = np.mean(A)
        mB = np.mean(B)
        sA = np.std(A, ddof=1) / math.sqrt(len(A))
        sB = np.std(B, ddof=1) / math.sqrt(len(B))
        var = (mA / mB) * ((sA / mA)**2 + (sB / mB)**2 - 2.0 * r * sA * sB / (mA * mB))
        return math.sqrt(var)

    def approximate_CIs(self, A, B, alpha=0.05):
        df = len(A) + len(B) - 2
        tval = s.InverseStudentT(df, 1 - alpha / 2.0)
        lower = np.mean(A) / np.mean(B) - tval * self.approximate_SDM(A, B)
        upper = np.mean(A) / np.mean(B) + tval * self.approximate_SDM(A, B)
        return lower, upper

    def df(self):
        return len(self.A) + len(self.B) - 2

    def __bootstrap(self, runs=5000):
        self.__bratios = np.zeros(runs)
        self.__breciprocals = np.zeros(runs)
        for i in range(runs):
            a = np.mean(np.random.choice(self.A, size=len(self.A), replace=True))
            b = np.mean(np.random.choice(self.B, size=len(self.B), replace=True))
            self.__bratios[i] = a / b
            self.__breciprocals[i] = b / a
        self.__bratios.sort()
        self.__breciprocals.sort()

    def CIs_bootstrap(self, runs=5000):
        self.__bootstrap(runs)
        self.__ratio_is_bootstrapped = True
        self.__booted_mean_ratio = np.mean(self.__bratios)
        self.__booted_mean_recip = np.mean(self.__breciprocals)
        self.__booted_sdm_ratio = np.std(self.__bratios, ddof=1)
        self.__booted_sdm_recip = np.std(self.__breciprocals, ddof=1)
        self.__runs = runs
        self.__ratio_bias = self.ratio() - np.mean(self.__bratios)
        self.ratio_lower95CI = self.__bratios[int(0.025 * runs)]
        self.ratio_upper95CI = self.__bratios[int(0.975 * runs)]
        self.reciprocal_lower95CI = self.__breciprocals[int(0.025 * runs)]
        self.reciprocal_upper95CI = self.__breciprocals[int(0.975 * runs)]
        
    def __repr__(self):
        repr_string = ('\nRatio = {0:.3g} +/- {1:.2g} (approximate SDM)'.
            format(self.ratio(), self.ratio_approxSDM()) +
            '\napproximate 95% confidence limits:\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(self.ratio_approxCIs(alpha=0.05)[0], self.ratio_approxCIs(alpha=0.05)[1]) +
            '\nReciprocal = {0:.3g} +/- {1:.2g} (approximate SDM)'.
            format(self.reciprocal(), self.reciprocal_approxSDM()) +
            '\napproximate 95% confidence limits:\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(self.reciprocal_approxCIs(alpha=0.05)[0], self.reciprocal_approxCIs(alpha=0.05)[1])
            )
        if self.__ratio_is_bootstrapped:
            repr_string += ('\n\nBootsrapping statistics; repeats = {0:d}'.format(self.__runs) +
            '\nRatio= {0:.3g} +/- {1:.2g} (bootstrapped SDM); bias= {2:.2g}'.
            format(self.ratio(), self.__booted_sdm_ratio, self.__ratio_bias) +
            '\n95% confidence limits (bootstrapped):\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(self.ratio_lower95CI, self.ratio_upper95CI) +
            '\nReciprocal= {0:.3g} +/- {1:.2g} (bootstrapped SDM)'.
            format(self.reciprocal(), self.__booted_sdm_recip) +
            '\n95% confidence limits (bootstrapped):\n\tlower= {0:.3g}; upper= {1:.3g}'.
            format(self.reciprocal_lower95CI, self.reciprocal_upper95CI)            
            )
        return repr_string

