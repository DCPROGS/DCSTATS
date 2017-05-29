import random
import math
from dcstats.statistics_EJ import simple_stats as mean_SD
from dcstats.statistics_EJ import InverseStudentT

class Hedges_d:
    ### calculation of Hedges' d (Hedges' unbiased g)
    ### see Nakagawa and Cuthill (2007) Biol. Rev.
    ### simple 95% confidence intervals
    ### bootstrap to get better (non-parametric) confidence intervals
    
    def __init__(self, sample1, sample2):
        ## sample1 and sample2 are the arrays to compare
        self.s1 = sample1
        self.s2 = sample2
        self.d = 0
        self.correction = 1
        self.SE_d = 0


    def approx_CI (self, paired=False):
        # 95% CI = ES - 1.96 * SE_d to ES + 1.96 * SE_d
        # ES is effect size: Hedge's d (the unbiased form)
        # se is asymptotic standard error for the ffect size
        # small samples (< 20) should use t distribution with appropriate df rather than 1.96
        # Nakagawa and Cuthill (2007) Biol. Rev.
        
        n1 = len (self.s1)
        n2 = len (self.s2)
        
        if self.SE_d == 0:
            self.asymptotic_SE_d_unpaired()
        
        #default for large samples
        t = 1.96

        if paired:
            df = n1 -1
        else:
            df = n1 + n2 - 2            #unpaired.
        
        if df < 120:
            print ("Small sample size (degrees of freedom < 120)")
            
            #for very large df, t at P > 0.975 approaches 1.96
            #see Stats_test.py
            #df = 10, t  = 2.23
            #df = 120, t = 1.98
            #df = 1000, t  = 1.962
            t = InverseStudentT (df, 0.975)

            print ("Degrees of Freedom: {:d} , t @ P_t-CDF = 0.975 : {:.2f} ".format(df, t))
                                     
        lower95CI = self.d - t * self.SE_d
        upper95CI = self.d + t * self.SE_d
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

        self.correction = 1.0 - 3.0 / (4 * (n1 + n2 - 2) - 1)
        
        #store answer
        self.d = biased_d * self.correction


    def bootstrap_CI (self, repeats, bCA=False):
        
        # repeats is the number of times that it is repeated.
        # bCA: bias-corrected and accelerated - recommended to improve pctile coverage
        # bCA not implemented yet
        
        hedges_d_bs = []     #unbiased, values from bootstrap
        
        n1m = len (self.s1) - 1     #we only use these below - simplifies
        n2m = len (self.s2) - 1
        correction = 1.0 - 3.0 / (4 * (n1m + n2m) - 1)
        
        for n in range (repeats):
            
            br1 = bootstrap(self.s1)
            br2 = bootstrap(self.s2)
        
            #means and SDs of bootstrap sampled distributions
            mbr1, sbr1 = mean_SD(br1)
            mbr2, sbr2 = mean_SD(br2)
        
            #need to call a function for Hedges_d that returns a value, not storing it
            #current alternative, just include here, it is so simple.
            s_pooled = math.sqrt((n2m * sbr2 ** 2 + n1m * sbr1 ** 2) / (n1m + n2m))
        
            #Hedges' g
            biased_d = (mbr2 - mbr1) / s_pooled
        
            # correction has no influence on the bootstrap distribution
            # so apply it later to save multiplications
            hedges_d_bs.append(biased_d)
        
        hedges_d_bs.sort()  # put the values into rank order
        
        lower95CI = hedges_d_bs[int(0.025 * repeats)] * correction
        upper95CI = hedges_d_bs[int(0.975 * repeats)] * correction
        return (lower95CI, upper95CI)
        


    def bias_corrected_bs_CI(self):
        pass

def bootstrap (sample):
    #if sample is [], then the same is returned
    l = len(sample)
    sup_s = sample * l             #concatenate l identical copies
    return random.sample(sup_s, l)


