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


class TTestContinuous(object):
    def __init__(self, X, Y, are_paired):
        """ 
        Parameters
        ----------
        X : observations in first trial, list of floats
        Y : observations in second trial, list of floats
        are_paired : are observations paired, boolean
        """
        
        self.X, self.Y = X, Y
        self.are_paired = are_paired
        # calculate mean and variance of nx and ny
        self.xbar, self.sdx, self.sdmx = mean(self.X), sd(self.X), sdm(self.X)
        self.ybar, self.sdy, self.sdmy = mean(self.Y), sd(self.Y), sdm(self.Y)

        self.nx, self.ny = len(X), len(Y)
        self.D = []
        if self.nx == self.ny:
            self.df = self.nx - 1
            for i in range(self.nx):
                self.D.append(self.X[i] - self.Y[i])    # differences for paired test
            self.dbar, self.sdd, self.sdmd = mean(self.D), sd(self.D), sdm(self.D)
        else:
            self.df = self.nx + self.ny - 2
            self.are_paired = False
            
        self.__t_test()
        
    def __t_test(self):
        if self.are_paired:               # And do a 2-sample paired t-test
            self.sdbar = self.sdd / sqrt(self.ny)
            self.tval = self.dbar / self.sdbar
            self.P = ttestPDF(self.tval, self.df)
        else:    # if not paired
            s = (self.sdx * self.sdx * (self.nx-1) + self.sdy * self.sdy * (self.ny-1)) / self.df
            sdiff = sqrt(s * (1.0 / self.nx + 1.0 / self.ny))
            adiff = fabs(self.xbar - self.ybar)
            self.tval = adiff / sdiff
            self.P = ttestPDF(self.tval, self.df)

    def __repr__(self):
        
        repr_string = ('n \t\t {0:d}      \t  {1:d}'.format(self.nx, self.ny) +
            '\nMean \t\t {0:.6f}    \t  {1:.6f}'.format(self.xbar, self.ybar) +
            '\nSD \t\t {0:.6f}     \t  {1:.6f}'.format(self.sdx, self.sdy) +
            '\nSDM \t\t {0:.6f}     \t  {1:.6f}'.format(self.sdmx, self.sdmy))
            
        if self.nx == self.ny:
            repr_string += ('\n\n Mean difference (dbar) = \t {0:.6f}'.format(self.dbar) +
                '\n  s(d) = \t {0:.6f} \t s(dbar) = \t {1:.6f}'.format(self.sdd, self.sdmd))

        if self.are_paired:
            repr_string += ('\n\n Paired Student''s t-test:' +
                '\n  t({0:d})= \t dbar / s(dbar) \t = \t {1:.6f}'.format(self.df, self.tval) +
                '\n  two tail P =\t {0:.6f}'.format(self.P))

        else:
            repr_string += ('\n\n Two-sample unpaired Student''s t-test:' +
                '\n t = \t {0:.6f}'.format(float(self.tval)) +
                '\n two tail P = \t {0:.6f}'.format(self.P))
            
        return repr_string
