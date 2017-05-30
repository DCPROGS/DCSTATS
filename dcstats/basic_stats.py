#!/usr/bin python
""" Some basic statistics functions. To be merged to statistics_EJ.py. """

from math import sqrt, fabs

from dcstats.statistics_EJ import incompleteBeta

def mean(X):
    """ Calculate mean of a list of values.
        Parameters
        ----------
        X : a list of values
        """
    return sum(X) / float(len(X))

def variance(X):
    """ Calculate variance.
        Parameters
        ----------
        X : a list of values
    """
    return sum([(i - mean(X)) ** 2 for i in X]) / (len(X) - 1)

def sd(X):
    """ Calculate standard deviation.
        Parameters
        ----------
        X : a list of values
    """   
    return sqrt(variance(X))   

def sdm(X):
    """ Calculate standard deviation of the mean.
        Parameters
        ----------
        X : a list of values
    """   
    return sd(X) / sqrt(len(X))

def ttestPDF(tval, df):
    """
    Calculate two-tailed t-test P-value.
    """
    x = df / (df + tval **2)
    return incompleteBeta(x, 0.5 * df, 0.5)

    
class TTestBinomial():
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
        self.__t_test()

    def __t_test(self):
        """" Use Gaussian approx to do 2 sample t test. """
        ppool = float(self.ir1 + self.ir2) / float(self.n1 + self.n2)
        self.sd1 = sqrt(self.p1 * (1.0 - self.p1) / float(self.n1))
        self.sd2 = sqrt(self.p2 * (1.0 - self.p2) / float(self.n2))
        sd1p = sqrt(ppool * (1.0 - ppool) / float(self.n1))
        sd2p = sqrt(ppool * (1.0 - ppool) / float(self.n2))
        sdiff = sqrt(sd1p * sd1p + sd2p * sd2p)
        self.tval = fabs(self.p1 - self.p2) / sdiff
        df = 100000    # to get Gaussian
        self.P = ttestPDF(self.tval, df)
        
    def __repr__(self):        
        repr_string = ('\n Set 1: {0:d} successes out of {1:d};'.format(self.ir1, self.n1) +
            '\n p1 = {0:.6f};   SD(p1) = {1:.6f}'.format(self.p1, self.sd1) +
            '\n Set 2: {0:d} successes out of {1:d};'.format(self.ir2, self.n2) +
            '\n p2 = {0:.6f};   SD(p2) = {1:.6f}'.format(self.p2, self.sd2) +
            '\n Observed difference between sets, p1-p2 = {0:.6f}'.format(self.p1 - self.p2) +
            '\n\n Observed 2x2 table:' +
            '\n  Set 1:    {0:d}      {1:d}      {2:d}'.format(self.ir1, self.if1, self.n1) +
            '\n  Set 2:    {0:d}      {1:d}      {2:d}'.format(self.ir2, self.if2, self.n2) +
            '\n  Total:    {0:d}      {1:d}      {2:d}'.format(
            self.ir1 + self.ir2, self.if1 + self.if2, self.n1 + self.n2) +
            '\n\n Two-sample unpaired test using Gaussian approximation to binomial:' +
            '\n standard normal deviate = {0:.6f}; two tail P = {1:.6f}.'.format(self.tval, self.P))
        return repr_string
