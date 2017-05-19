#!/usr/bin python

'fieller.py -- To calculate Fieller''s theorem\
               Converted from FORTRAN version FIELLER.FOR'

import math
import statistics_EJ as s

__author__="remis"
__date__ ="$30-Apr-2009 09:51:16$"

def calc_t(df, power):
    """wrapper for function in statistics.EJ.py code"""
        
    return s.InverseStudentT(df, power)

class Fieller(object):

    introd = 'FIELLER: calculates confidence limits for a ratio \
according Fieller''s theorem (see Finney\'s book). Output includes the approximate \
SD of the ratio r = a / b, given the SD of a (the numerator) and of b (the denominator)\
 and the correlation coefficient between a & b (zero if \
they are independent). \n\
Fieller requires the t-statistic which can be provided from a table \
or calculated from alpha and the degrees of freedom. \
Alpha-level deviation is for two tailed distribution (e.g. 0.05 leaves 90% area)\n'

    dict = {}

    def setInData(self,a, b, sa, sb, r, tval):
        'Puts initial data into Fiellers class dictionary.'

        self.dict['a'] = a
        self.dict['b'] = b
        self.dict['sa'] = sa
        self.dict['sb'] = sb
        self.dict['r'] = r
        self.dict['tval'] = tval

    def calcFieller(self, a, b, sa, sb, r, tval):
        'Fieller formula calculator.'

        va = sa * sa
        vb = sb * sb
        cov = r * sa * sb
        g = tval * tval * vb /(b * b)
        ratio = a / b
        rat2 = ratio * ratio
        # Write disc in a way that does not appear to divide by vb
        # (which actually cancels) so OK to use vb=0
        # disc=va - 2.0*ratio*cov + rat2*vb - g*(va-cov*cov/vb)
        disc = va - 2.0 * ratio * cov + rat2 * vb - g * (va - r * r * va)
        
        clower = 0
        cupper = 0
        appsd = 0
        applo = 0
        apphi = 0
        cvr = 0
        dlow = 0
        dhi = 0
        
        if disc >= 0:
            d = (tval / b) * math.sqrt(disc)
            # Write pre in a way that does not appear to divide by vb
            # (which actually cancels) so OK to use vb=0 (use g=tval*tval*vb/(b*b))
            #	pre=ratio - g*cov/vb
            pre = ratio - (tval * tval * r * sa * sb) / (b * b)
            f = 1.0 / (1.0 - g)
            clower = f * (pre - d)
            cupper = f * (pre + d)
            dlow = clower - ratio
            dhi = cupper - ratio
            # Approximation for small g
            appsd = math.sqrt(va + rat2 * vb - 2.0 * ratio * cov) / b
            applo = ratio - tval * appsd
            apphi = ratio + tval * appsd
            cvr = 100.0 * appsd / ratio

        return g, ratio, disc, clower, cupper, dlow, dhi, appsd, applo, apphi, cvr

    
    def setResult(self, g, ratio, disc, clower, cupper, dlow, dhi, appsd, applo, apphi, cvr):
        'Puts result into Fiellers class dictionary.'

        self.dict['g'] = g
        self.dict['ratio'] = ratio
        self.dict['disc'] = disc
        self.dict['clower'] = clower
        self.dict['cupper'] = cupper
        self.dict['dlow'] = dlow
        self.dict['dhi'] = dhi
        self.dict['appsd'] = appsd
        self.dict['applo'] = applo
        self.dict['apphi'] = apphi
        self.dict['cvr'] = cvr

    def __init__(self, a, b, sa, sb, r, tval):
        self.setInData(a, b, sa, sb, r, tval)
        g, ratio, disc, clower, cupper, dlow, dhi, appsd, applo, apphi, cvr = self.calcFieller(a, b, sa, sb, r, tval)
        self.setResult(g, ratio, disc, clower, cupper, dlow, dhi, appsd, applo, apphi, cvr)

if __name__ == "__main__":

    print (introd)
