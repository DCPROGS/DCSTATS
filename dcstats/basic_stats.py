#!/usr/bin python
""" Some basic statistics functions. To be merged to statistics_EJ.py. """

#math import sqrt, fabs, erf, exp
import math

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
    return math.sqrt(variance(X))   

def sdm(X):
    """ Calculate standard deviation of the mean.
        Parameters
        ----------
        X : a list of values
    """   
    return sd(X) / math.sqrt(len(X))

def _pdf(x, mu, sd):
    """Normal distribution density """
    return 1 / (sd * math.sqrt(2 * math.pi)) * math.exp( - (x - mu)**2 / (2 * sd**2)) 

def _cdf(x, mu, sd):
    """Cumulative density function for normal distribution """
    return (1.0 + math.erf((x - mu) / (sd * math.sqrt(2.0)))) / 2.0

def _phi(x):
    """Cumulative density function for the standard normal distribution """
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def _beta_two_tail(m1, s1, n1, m2, s2, n2):
    """ beta-error two-tailed for alpha = 0.05"""
    z025 = 1.96
    z = (m1 - m2) / math.sqrt(s1**2  / n1 + s2**2 / n2)
    return _phi(z025 - z) - _phi(-z025 - z)

def power(m1, s1, n1, m2, s2, n2):
    """Statistical power (1 - beta error)"""
    return 1 - _beta_two_tail(m1, s1, n1, m2, s2, n2)

def ci95lower(X):
    """ Calculate 95% confidence interval (lower) for the mean.
        Parameters
        ----------
        X : a list of values
    """ 
    z = 1.96 # z*-value from the standard normal distribution for 95% confidence level
    #TODO: allow calculation for desired confidence level
    return mean(X) - z * sdm(X) 

def ci95upper(X):
    """ Calculate 95% confidence intervals (upper) for the mean.
        Parameters
        ----------
        X : a list of values
    """ 
    z = 1.96 # z*-value from the standard normal distribution for 95% confidence level
    #TODO: allow calculation for desired confidence level
    return mean(X) + z * sdm(X) 


def ttest_independent(X, Y):
    """Calculate t-value and probability for un-paired t-test."""
    df = len(X) + len(Y) - 2
    xbar, sdx = mean(X), sd(X)
    ybar, sdy = mean(Y), sd(Y)
    tval = (xbar - ybar) / math.sqrt(sdx**2 / len(X) + sdy**2 / len(Y))
    P = ttestPDF(math.fabs(tval), df)
    return tval, P, df

def ttest_paired(X, Y):
    """Calculate t-value and probability for paired t-test."""
    D = []
    if len(X) == len(Y):
        for i in range(len(X)):
            D.append(X[i] - Y[i])    # differences for paired test
    df = len(D) - 1
    tval = mean(D) / sdm(D)
    P = ttestPDF(tval, df)
    return tval, P, df

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
        self.sd1 = math.sqrt(self.p1 * (1.0 - self.p1) / float(self.n1))
        self.sd2 = math.sqrt(self.p2 * (1.0 - self.p2) / float(self.n2))
        sd1p = math.sqrt(ppool * (1.0 - ppool) / float(self.n1))
        sd2p = math.sqrt(ppool * (1.0 - ppool) / float(self.n2))
        sdiff = math.sqrt(sd1p * sd1p + sd2p * sd2p)
        self.tval = math.fabs(self.p1 - self.p2) / sdiff
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
        self.D = []
        if len(self.X) == len(self.Y):
            for i in range(len(self.X)):
                self.D.append(self.X[i] - self.Y[i])    # differences for paired test
            self.dbar, self.sdd, self.sdmd = mean(self.D), sd(self.D), sdm(self.D)
        else:
            self.dbar = math.fabs(mean(self.X) - mean(self.Y))
            self.are_paired = False
        self.__t_test()
        
    def __t_test(self):
        if self.are_paired:               # And do a 2-sample paired t-test
            self.tval, self.P, self.df = ttest_paired(self.X, self.Y)
        else:    # if not paired
            self.tval, self.P, self.df = ttest_independent(self.X, self.Y)

    def __repr__(self):
        
        repr_string = ('n \t\t {0:d}     \t{1:d}'.format(len(self.X), len(self.Y)) +
            '\nMean \t\t {0:.6f}    \t  {1:.6f}'.format(mean(self.X), mean(self.Y)) +
            '\nSD \t\t {0:.6f}     \t  {1:.6f}'.format(sd(self.X), sd(self.Y)) +
            '\nSDM \t\t {0:.6f}     \t  {1:.6f}'.format(sdm(self.X), sdm(self.Y)) +
            '\n95% confidence intervals:' +
            '\nlower \t\t {0:.6f}    \t  {1:.6f}'.format(ci95lower(self.X), ci95lower(self.Y)) +
            '\nupper \t\t {0:.6f}    \t  {1:.6f}'.format(ci95upper(self.X), ci95upper(self.Y)))
            
        if len(self.X) == len(self.Y):
            repr_string += ('\n\n Mean difference (dbar) = \t {0:.6f}'.format(self.dbar) +
                '\n  s(d) = \t {0:.6f} \t s(dbar) = \t {1:.6f}'.format(self.sdd, self.sdmd))

        if self.are_paired:
            repr_string += ('\n\n Paired Student''s t-test:' +
                '\n  t({0:d})= \t dbar / s(dbar) \t = \t {1:.6f}'.format(self.df, self.tval) +
                '\n  two tail P =\t {0:.6f}'.format(self.P))

        else:
            repr_string += ('\n\n Two-sample unpaired Student''s t-test:' +
                '\n t = \t {0:.6f}'.format(float(self.tval)) +
                '\n two tail P = \t {0:.3E}'.format(self.P) +
                '\n\n statistical power = {0:.3f}'.
                format(power(mean(self.X), sd(self.X), len(self.X), 
                             mean(self.Y), sd(self.Y), len(self.X))))
            
        return repr_string
