import random

Class Hedges_G(self):

    def bootstrap (sample):
        #if sample is [], then the same is returned
        l = len(sample)
        sup_s = sample*l
        return random.sample(sup_s, l)

    def simple_bs_CI (self, sample1, sample2, function, repeats):
    
        # sample 1 and sample 2 are the two arrays of numbers
        # function is an object that returns the function of interest
        # repeats is the number of times that it is repeated.
        
        
        
    def bias-corrected_bs_CI
    
    
    def hedges_g (self,x,y):
        mx = avg(x)
        my = avg(y)
        #pooled variance?
        s_xy_star = (len(x)etc)
        return (mx-my)/s_xy_star
