#!/usr/bin python
"""fieller.py -- To calculate Fieller''s theorem\
               Converted from FORTRAN version FIELLER.FOR"""

import math
import dcstats.statistics_EJ as s

__author__="remis"
__date__ ="$30-Apr-2009 09:51:16$"

## This wrapper is not used in this module.
#def calc_t(df, power):
#    """wrapper for function in statistics.EJ.py code"""        
#    return s.InverseStudentT(df, power)

class Fieller(object):

    introd = 'FIELLER: calculates confidence limits for a ratio \
according Fieller''s theorem (see Finney\'s book). Output includes the approximate \
SD of the ratio r = a / b, given the SD of a (the numerator) and of b (the denominator)\
 and the correlation coefficient between a & b (zero if \
they are independent). \n\
Fieller requires the t-statistic which can be provided from a table \
or calculated from alpha and the degrees of freedom. \
Alpha-level deviation is for two tailed distribution (e.g. 0.05 leaves 90% area)\n'

    def __init__(self, a, b, sa, sb, r, alpha, Ntot):
        self.a, self.b = a, b
        self.sa, self.sb = sa, sb
        self.r = r
        self.Ntot = Ntot
        self.alpha = alpha
        self.__calculate_t()
        self.calcFieller()

    def __calculate_t(self):
        self.df = self.Ntot - 2
        two_tail = 1 - float(self.alpha)
        self.tval = s.InverseStudentT(self.df, two_tail)

    def calcFieller(self):
        'Fieller formula calculator.'
        va = self.sa * self.sa
        vb = self.sb * self.sb
        cov = self.r * self.sa * self.sb
        self.g = self.tval * self.tval * vb /(self.b * self.b)
        self.ratio = self.a / self.b
        rat2 = self.ratio * self.ratio
        # Write disc in a way that does not appear to divide by vb
        # (which actually cancels) so OK to use vb=0
        # disc=va - 2.0*ratio*cov + rat2*vb - g*(va-cov*cov/vb)
        disc = va - 2.0 * self.ratio * cov + rat2 * vb - self.g * (va - self.r * self.r * va)
        
        self.clower, self.cupper = 0.0, 0.0
        self.appsd, self.applo = 0.0, 0.0
        self.apphi = 0.0
        self.cvr = 0.0
        self.dlow, self.dhi = 0.0, 0.0
        
        if disc >= 0:
            d = (self.tval / self.b) * math.sqrt(disc)
            # Write pre in a way that does not appear to divide by vb
            # (which actually cancels) so OK to use vb=0 (use g=tval*tval*vb/(b*b))
            #	pre=ratio - g*cov/vb
            pre = self.ratio - (self.tval * self.tval * self.r * self.sa * self.sb) / (self.b * self.b)
            f = 1.0 / (1.0 - self.g)
            self.clower = f * (pre - d)
            self.cupper = f * (pre + d)
            self.dlow = self.clower - self.ratio
            self.dhi = self.cupper - self.ratio
            # Approximation for small g
            self.appsd = math.sqrt(va + rat2 * vb - 2.0 * self.ratio * cov) / self.b
            self.applo = self.ratio - self.tval * self.appsd
            self.apphi = self.ratio + self.tval * self.appsd
            if self.ratio != 0:
                self.cvr = 100.0 * self.appsd / self.ratio

    def __repr__(self):
        return ('\nResult: ' +
            '\n Ratio (=a/b) = {0:.6f}'.format(self.ratio) +
            '\n g = {0:.6f}; \n degree of freedom  = {1:d}; \n t(df, alpha) = {2:.6f}'.
            format(self.g, int(self.df), self.tval) +
            '\n\n Confidence limits: lower {0:.6f}, upper {1:.6f}'.format(self.clower, self.cupper) +
            '\n i.e deviations: lower {0:.6f}, upper {1:.6f}'.format(self.dlow, self.dhi) + 
            '\n Approximate SD of ratio = {0:.6f}'.format(self.appsd) +
            '\n Approximate CV of ratio (%) = {0:.6f}'.format(self.cvr) + 
            '\n Approximate limits: lower {0:.6f}, upper {0:.6f}'.format(self.applo, self.apphi))
