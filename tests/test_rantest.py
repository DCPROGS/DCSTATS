#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dcstats.rantest import RantestBinomial
from dcstats.rantest import RantestContinuous
#from test_statistics import isclose

def test_regression_rantest_continuos():
    # Samples from treatment T1 and T2
    T1 = [100, 108, 119, 127, 132, 135, 136] #, 164]
    T2 = [122, 130, 138, 142, 152, 154, 176]
    nran = 5000
    rnt = RantestContinuous(T1, T2, True)    
    rnt.run_rantest(nran)
    assert rnt.pg1 == 1.0
    assert (rnt.pa1 > 0.01) and (rnt.pa1 < 0.025)
    assert (rnt.ne2 > 50) and (rnt.ne2 < 100)

    rnt = RantestContinuous(T1, T2, False)
    rnt.run_rantest(nran)    
    assert (rnt.pg1 > 0.98) and (rnt.pg1 < 1.0)
    assert (rnt.pa1 > 0.015) and (rnt.pa1 < 0.035)
    assert (rnt.ne2 > 0) and (rnt.ne2 < 20)
   

def test_regression_rantest_binomial():
    
    ir1, if1 = 3, 4
    ir2, if2 = 4, 5
    nran = 5000
    rnt = RantestBinomial(ir1, if1, ir2, if2)
    rnt.run_rantest(nran)

    assert (rnt.pg1 > 0.6) and (rnt.pg1 < 0.8)
    assert (rnt.pl1 > 0.6) and (rnt.pl1 < 0.8)
    assert (rnt.pe1 > 0.2) and (rnt.pe1 < 0.4)
    assert (rnt.ne1 > 1800) and (rnt.ne1 < 2000)
 