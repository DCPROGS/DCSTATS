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

    rnt = RantestBinomial(ir1, if1, ir2, if2)
    rnt.tTestBinomial()
    rnt.doRantestBinomial(2, nran)
    #rntd = rnt.dict
    
    result1 = (rnt.ir1, rnt.n1, rnt.p1, rnt.sd1, rnt.ir2, rnt.n2, rnt.p2, rnt.sd2, rnt.p1 - rnt.p2)
    
    print(' Set 1: %d successes out of %d; \
        \n p1 = %f;   SD(p1) = %f \
        \n Set 2: %d successes out of %d; \
        \n p2 = %f;   SD(p2) = %f \
        \n Observed difference between sets, p1-p2 = %f' %result1)
        
    assert isclose(rnt.p1, 0.428571, rel_tol=0.0001)
    assert isclose(rnt.p2, 0.444444, rel_tol=0.0001)
    assert isclose(rnt.sd1, 0.187044, rel_tol=0.0001)
    assert isclose(rnt.sd2, 0.165635, rel_tol=0.0001)
        
    irt = rnt.ir1 + rnt.ir2
    ift = rnt.n1 + rnt.n2 - rnt.ir1 - rnt.ir2
    nt = rnt.n1 + rnt.n2
    result2 = (rnt.ir1, rnt.if1, rnt.n1, rnt.ir2, rnt.if2, rnt.n2, irt, ift, nt)

    print('\n Observed 2x2 table: \
        \n  Set 1:    %d      %d      %d \
        \n  Set 2:    %d      %d      %d \
        \n  Total:    %d      %d      %d' %result2)

    print('\n Two-sample unpaired test using Gaussian approximation to binomial: \
        \n standard normal deviate = {0:.6f}; two tail P = {1:.6f}.'.format(rnt.tval, rnt.P))
    
    assert isclose(rnt.tval, 0.063492, rel_tol=0.0001)
    assert isclose(rnt.P, 0.949375, rel_tol=0.0001)

    print('\n {0:d} randomisations \
        \n P values for difference between sets are: \
        \n  r1 greater than or equal to observed: P = {1:.6f} \
        \n  r1 less than or equal to observed: P = {2:.6f} \
        \n  r1 equal to observed: number = {3:d} (P = {4:.6f})'.format(
        rnt.nran, rnt.pg1, rnt.pl1, rnt.ne1, rnt.pe1))

