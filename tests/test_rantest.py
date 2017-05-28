#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rantest import RantestBinomial
from rantest import RantestContinuous
from test_statistics import isclose

def test_regression_rantest_continuos():
    # Samples from treatment T1 and T2
    T1 = [100, 108, 119, 127, 132, 135, 136] #, 164]
    T2 = [122, 130, 138, 142, 152, 154, 176]
    nran = 5000
    are_paired = True
    rnt = RantestContinuous(T1, T2, are_paired)
    
    assert isclose(rnt.xbar, 122.428571, rel_tol=0.00001)
    assert isclose(rnt.ybar, 144.857143, rel_tol=0.00001)
    assert isclose(rnt.sdx, 14.010200, rel_tol=0.00001)
    assert isclose(rnt.sdy, 17.808505, rel_tol=0.00001)
    assert isclose(rnt.sex, 5.295358, rel_tol=0.00001)
    assert isclose(rnt.sey, 6.730982, rel_tol=0.00001)
        
    rnt.run_rantest(nran)            
    assert isclose(rnt.tval, -7.325473, rel_tol=0.000001)
    
    are_paired = False
    rnt = RantestContinuous(T1, T2, are_paired)
    rnt.run_rantest(nran)
    #print(rnt)
    #assert 0 == 1
    

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
 