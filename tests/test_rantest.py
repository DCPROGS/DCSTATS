#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

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
    
    ir1, if1 = 3, 4
    ir2, if2 = 4, 5
    nran = 5000
    rnt = RantestBinomial(ir1, if1, ir2, if2)
    rnt.run_rantest(nran)
    
    assert isclose(rnt.p1, 0.428571, rel_tol=0.0001)
    assert isclose(rnt.p2, 0.444444, rel_tol=0.0001)
    assert isclose(rnt.sd1, 0.187044, rel_tol=0.0001)
    assert isclose(rnt.sd2, 0.165635, rel_tol=0.0001)
    assert isclose(rnt.tval, 0.063492, rel_tol=0.0001)
    assert isclose(rnt.P, 0.949375, rel_tol=0.0001)

    assert (rnt.pg1 > 0.6) and (rnt.pg1 < 0.8)
    assert (rnt.pl1 > 0.6) and (rnt.pl1 < 0.8)
    assert (rnt.pe1 > 0.2) and (rnt.pe1 < 0.4)
    assert (rnt.ne1 > 1800) and (rnt.ne1 < 2000)
 