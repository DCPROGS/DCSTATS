from Hedges import Hedges_d
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

    sample_size = 200
    count_error = math.sqrt(sample_size)
    
    m1 = 1
    m2 = 3
    sig = 2
    
    s1 = generate_sample (sample_size, m1, sig)
    s2 = generate_sample (sample_size, m2, sig)

    h_testing = Hedges_d(s1, s2)
    h_testing.hedges_d_unbiased()
    approx_95CI_lower, approx_95CI_upper = h_testing.approx_CI()
    bs_95CI_lower, bs_95CI_upper = h_testing.bootstrap_CI(5000)

    print ("h_testing.d = ", h_testing.d)
    print (approx_95CI_lower, bs_95CI_lower)
    print (approx_95CI_upper, bs_95CI_upper)

    assert close_enough(approx_95CI_lower, bs_95CI_lower, count_error)
    assert close_enough(approx_95CI_upper, bs_95CI_upper, count_error)
    assert close_enough(h_testing.d, (m2 - m1) / sig, count_error)
