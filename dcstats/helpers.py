import dcstats.rantest as rantest
from dcstats.Hedges import Hedges_d
from dcstats.fieller import Fieller
from dcstats.basic_stats import TTestContinuous, TTestBinomial

def calculate_ttest_hedges(X, Y, are_paired=False):
    """ Run Student's two-tailed t-test for a difference between two samples
        and calculate Hedges effect size. Return results as string. """
    ttc = TTestContinuous(X, Y, are_paired)
    #calculation of hedges d and approximate 95% confidence intervals
    #not tested against known values yet AP 170518
    hedges_calculation = Hedges_d(X, Y)
    hedges_calculation.hedges_d_unbiased()
    #lowerCI, upperCI = hedges_calculation.approx_CI(self.paired)
    #paired needed for degrees of freedom
    hedges_calculation.bootstrap_CI(5000)
    #option to have bootstrap calculated CIs should go here
    return str(ttc) + str(hedges_calculation)


def calculate_rantest_continuous(nran, X, Y, are_paired=False):
    """ Run randomisation test and return result as string. """
    rnt = rantest.RantestContinuous(X, Y, are_paired)
    rnt.run_rantest(nran)
    return rnt.randiff, str(rnt)


def calculate_rantest_binary(nran, ir1, if1, ir2, if2):
    """ Run randomisation test and return result as string. """
    ttb = TTestBinomial(ir1, if1, ir2, if2)
    rnt = rantest.RantestBinomial(ir1, if1, ir2, if2)
    rnt.run_rantest(nran)
    return str(ttb) + str(rnt)

def calculate_fieller(a, b, sa, sb, r, alpha, Ntot):
    return str(Fieller(a, b, sa, sb, r, alpha, Ntot))