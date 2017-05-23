#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import math
import random

from rantest import Rantest
from rantest import RantestBinomial
from rantest import RantestContinuous
from test_statistics import isclose

def test_regression_rantest_continuos():
    # Samples from treatment T1 and T2
    T1 = [100, 108, 119, 127, 132, 135, 136] #, 164]
    T2 = [122, 130, 138, 142, 152, 154, 176]
    nset = 1
    in_data = []
    in_data.append(nset)
    for j in range(0, nset):
        in_data.append(len(T1))
        in_data.append(len(T2))
        titled = 'Set'
        titlex = 'Sample 1'
        titley = 'Sample 2'
        in_data.append(titled)
        in_data.append(titlex)
        in_data.append(titley)
        in_data.append(T1)
        in_data.append(T2)

    jset = 1
    nran = 5000
    are_paired = True
    rnt = RantestContinuous()
    xobs, yobs = rnt.setContinuousData(in_data, nran, jset, are_paired)
    
    rnt.tTestContinuous(xobs, yobs, are_paired)
    print('n \t\t %(nx)d      \t  %(ny)d \
        \nMean \t\t %(xbar)f    \t  %(ybar)f \
        \nSD \t\t %(sdx)f     \t  %(sdy)f \
        \nSDM \t\t %(sex)f     \t  %(sey)f' %rnt.dict)
    
    assert isclose(rnt.dict['xbar'], 122.428571, rel_tol=0.00001)
    assert isclose(rnt.dict['ybar'], 144.857143, rel_tol=0.00001)
    assert isclose(rnt.dict['sdx'], 14.010200, rel_tol=0.00001)
    assert isclose(rnt.dict['sdy'], 17.808505, rel_tol=0.00001)
    assert isclose(rnt.dict['sex'], 5.295358, rel_tol=0.00001)
    assert isclose(rnt.dict['sey'], 6.730982, rel_tol=0.00001)
        
    rnt.doRantestContinuous(xobs, yobs, are_paired, nran)
    randiff = rnt.dict['randiff']
    
    if rnt.dict['nx'] == rnt.dict['ny'] and are_paired:
    #result2 = (rnt.dbar, rnt.sdd, rnt.sed)
        print('\n\n Mean difference (dbar) = \t %(dbar)f \
            \n  s(d) = \t %(sdd)f \t s(dbar) = \t %(sed)f' %rnt.dict)
            
    if are_paired:
    #result3 = (rnt.df, rnt.dbar, rnt.sdbar, rnt.tval, rnt.P)
        print('\n  t(%(df)d)= \t %(dbar)f \t / \t%(sdbar)f \t = \t %(tval)f \
            \n  two tail P =\t %(P)f' %rnt.dict)
            
    assert isclose(rnt.dict['tval'], -7.325473, rel_tol=0.000001)
            
    print('\n\n'+rnt.dict['RanPaired'])
    print('\n\n   %(nran)d randomisations \
        \n P values for difference between means \
        \n  greater than or equal to observed: P = \t %(pg1)f \
        \n  less than or equal to observed: P = \t %(pl1)f \
        \n  greater than or equal in absolute value to observed: P = \t %(pa1)f \
        \n  Number equal to observed = %(ne1)d (P= %(pe1)f) \
        \n  Number equal in absolute value to observed = %(ne2)d (P= %(pe2)f)' %rnt.dict)
    
def test_regression_rantest_binomial():
    
    ir1 = 3
    if1 = 4
    ir2 = 4
    if2 = 5
    nran = 5000
    
    n1 = ir1 + if1
    n2 = ir2 + if2

    rnt = RantestBinomial()
    rnt.tTestBinomial(n1, n2, ir1, ir2)
    rnt.doRantestBinomial(n1, n2, ir1, ir2, 2, nran)
    rntd = rnt.dict
    
    result1 = (rntd['ir1'], rntd['n1'], rntd['p1'], rntd['sd1'], rntd['ir2'], rntd['n2'], rntd['p2'], rntd['sd2'], rntd['p1'] - rntd['p2'])
    
    print(' Set 1: %d successes out of %d; \
        \n p1 = %f;   SD(p1) = %f \
        \n Set 2: %d successes out of %d; \
        \n p2 = %f;   SD(p2) = %f \
        \n Observed difference between sets, p1-p2 = %f' %result1)
        
    assert isclose(rntd['p1'], 0.428571, rel_tol=0.0001)
    assert isclose(rntd['p2'], 0.444444, rel_tol=0.0001)
    assert isclose(rntd['sd1'], 0.187044, rel_tol=0.0001)
    assert isclose(rntd['sd2'], 0.165635, rel_tol=0.0001)
        
    irt = rntd['ir1'] + rntd['ir2']
    ift = rntd['n1'] + rntd['n2'] - rntd['ir1'] - rntd['ir2']
    nt = rntd['n1'] + rntd['n2']
    result2 = (rntd['ir1'], if1, rntd['n1'], rntd['ir2'], if2, rntd['n2'], irt, ift, nt)

    print('\n Observed 2x2 table: \
        \n  Set 1:    %d      %d      %d \
        \n  Set 2:    %d      %d      %d \
        \n  Total:    %d      %d      %d' %result2)

    print('\n Two-sample unpaired test using Gaussian approximation to binomial: \
        \n standard normal deviate = %(tval)f; two tail P = %(P)f.' %rntd)
    
    assert isclose(rntd['tval'], 0.063492, rel_tol=0.0001)
    assert isclose(rntd['P'], 0.949375, rel_tol=0.0001)

    print('\n %(nran)d randomisations \
        \n P values for difference between sets are: \
        \n  r1 greater than or equal to observed: P = %(pg1)f \
        \n  r1 less than or equal to observed: P = %(pl1)f \
        \n  r1 equal to observed: number = %(ne1)d (P = %(pe1)f)' %rntd)

