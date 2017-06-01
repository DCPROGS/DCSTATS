#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt, fabs

from test_statistics import isclose
from dcstats.basic_stats import ttest_independent, ttest_paired
from dcstats.basic_stats import TTestBinomial, TTestContinuous
    
def test_ttest_P_paired():
    X = [2, 4, 6]
    Y = [1, 2, 3]
    tval, P, df = ttest_paired(X, Y)
    assert isclose(tval, 3.464101615137754, rel_tol=0.0000001)
    assert isclose(P, 0.07417990022744862, rel_tol=0.0000001)

def test_ttest_P_unpaired():
    X = [1, 2, 3]
    Y = [1, 4, 6]
    tval, P, df = ttest_independent(X, Y)
    assert isclose(tval, -1.06600358178, rel_tol=0.0000001)
    assert isclose(P, 0.346490370194, rel_tol=0.0000001)
    
def test_regression_ttest_binomial():
    
    ir1, if1 = 3, 4
    ir2, if2 = 4, 5
    ttb = TTestBinomial(ir1, if1, ir2, if2)
    
    assert isclose(ttb.p1, 0.428571, rel_tol=0.0001)
    assert isclose(ttb.p2, 0.444444, rel_tol=0.0001)
    assert isclose(ttb.sd1, 0.187044, rel_tol=0.0001)
    assert isclose(ttb.sd2, 0.165635, rel_tol=0.0001)
    assert isclose(ttb.tval, 0.063492, rel_tol=0.0001)
    assert isclose(ttb.P, 0.949375, rel_tol=0.0001)

def test_regression_ttest_continuos():
    # Samples from treatment T1 and T2
    T1 = [100, 108, 119, 127, 132, 135, 136] #, 164]
    T2 = [122, 130, 138, 142, 152, 154, 176]
    are_paired = True
    ttc = TTestContinuous(T1, T2, are_paired)
    assert isclose(ttc.tval, -7.325473, rel_tol=0.000001)
    assert isclose(ttc.P, 0.000331, rel_tol=0.01)
