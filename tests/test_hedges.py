from dcstats.Hedges import Hedges_d
from dcstats.statistics_EJ import simple_stats as mean_SD
import random
import math

def generate_sample (length, mean, sigma):
    #generate a list of normal distributed samples
    sample = []
    for n in range(length):
        sample.append(random.gauss(mean, sigma))

    return sample

def close_enough (a, b, count_error):
    if math.fabs (a - b) < math.fabs((a + b) / (count_error * 2)) :
        return True
    else:
        return False

def test_gaussian_case():
    
    SDs = [0.2, 0.5, 1]         #expect d = 5, 2, 1 , expected to fail on low d
    
    sample_size = 200
    count_error = math.sqrt(sample_size)
    
    m1 = 1
    m2 = 2
    test_num
    for sig in SDs:
        
        s1 = generate_sample (sample_size, m1, sig)
        s2 = generate_sample (sample_size, m2, sig)

        h_testing = Hedges_d(s1, s2)
        
        h_testing.hedges_d_unbiased()               #answer is in self.d
        approx_95CI_lower, approx_95CI_upper = h_testing.approx_CI()
        bs_95CI_lower, bs_95CI_upper = h_testing.bootstrap_CI(5000)

        print (mean_SD(s1), mean_SD(s2))
        print ("h_testing.d, analytic, correction = ", h_testing.d, (m2 - m1) / sig, h_testing.correction)
        print ("lower: approx, bootstrap", approx_95CI_lower, bs_95CI_lower)
        print ("upper: approx, bootstrap", approx_95CI_upper, bs_95CI_upper)

        #bootstrap is similar at high d but gives wider intervals at low d
        assert close_enough(approx_95CI_lower, bs_95CI_lower, count_error)
        assert close_enough(approx_95CI_upper, bs_95CI_upper, count_error)
        assert close_enough(h_testing.d, (m2 - m1) / sig, count_error)
