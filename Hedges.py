import random
import math
from statistics_EJ import simple_stats as mean_SD

class Hedges_d:
    ### calculation of Hedges' d (Hedges' unbiased g)
    ### see Nakagawa and Cuthill (2007) Biol. Rev.
    ### simple 95% confidence intervals
    ### TODO : bootstrap to get better (non-parametric) confidence intervals
    
    def __init__(self, sample1, sample2):
        ## sample1 and sample2 are the arrays to compare
        self.s1 = sample1
        self.s2 = sample2
        self.d = 0
        self.SE_d = 0

    def approx_CI (self):
        # 95% CI = ES - 1.96 * SE_d to ES + 1.96 * SE_d
        # ES is effect size: Hedge's d (the unbiased form)
        # se is asymptotic standard error for the ffect size
        # small samples (< 20) should use t distribution with appropriate df rather than 1.96
        # Nakagawa and Cuthill (2007) Biol. Rev.
        
        if self.SE_d == 0:
            self.asymptotic_SE_d_unpaired()
        
        if len (self.s1) < 20 or len (self.s2) < 20:
            print ("Small sample size, should use correct df for approx 95% CI [not yet implemented]")
        
        lower95CI = self.d - 1.96 * self.SE_d
        upper95CI = self.d + 1.96 * self.SE_d
        return (lower95CI, upper95CI)
    
    def asymptotic_SE_d_unpaired (self):
        # Hedges 1981, via Nakagawa and Cuthill (2007) Biol. Rev., Table 3
        # SE_d = [ (n1 + n2) / (n1 * n2) + d^2 / (2 * (n1 + n2 -2)) ] ^ 0.5
        
        n1 = len (self.s1)
        n2 = len (self.s2)
        
        if self.d == 0:
            self.hedges_d_unbiased()
        
        first_term = (n1 + n2) / (n1 * n2)
        second_term = self.d ** 2 / (2 * (n1 + n2 - 2))
    
        self.SE_d = math.sqrt(first_term + second_term)
    

    def hedges_d_unbiased (self):

        #d_unbiased = d_biased [ 1 - 3/ (4 * ( n1 + n2 - 2)-1)]
        #from Nakagawa and Cuthill (2007) Biol. Rev.
        
        #count each time to make formulas easier to read
        n1 = len (self.s1)
        n2 = len (self.s2)
        #means and standard deviations
        m1, s1 = mean_SD(self.s1)
        m2, s2 = mean_SD(self.s2)
        
        #pooled variance
        s_pooled = math.sqrt(((n2 - 1) * s2 ** 2 + (n1 - 1) * s1 ** 2) / (n1 + n2 - 2))

        #Hedges' g
        biased_d = (m2 - m1) / s_pooled

        correction = 1 - 3 / (4 * (n1 + n2 - 2) - 1)
        
        #store answer
        self.d = biased_d * correction

    ##following is not used yet
    def bootstrap_CI (self, function, repeats):
        
        # function is an object that returns the function of interest
        # repeats is the number of times that it is repeated.
        pass
    
    def bias_corrected_bs_CI(self):
        pass

    def bootstrap (sample):
        #if sample is [], then the same is returned
        l = len(sample)
        sup_s = sample * l
        return random.sample(sup_s, l)


