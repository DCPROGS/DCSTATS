#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt, fabs

from test_statistics import isclose
import dcstats.statistics_EJ as s
from dcstats.basic_stats import mean, sd, sdm, ttestPDF
from dcstats.basic_stats import TTestBinomial
    
def test_ttest_P_paired():
    D = [1, 2, 3]
    df = len(D) - 1
    dbar, dsdm = mean(D), sdm(D)
    print(dbar, dsdm)
    tval = dbar / dsdm
    print(tval)
    assert isclose(tval, 3.464101615137754, rel_tol=0.0000001)
    
    P = ttestPDF(tval, df)
    print(P)
    assert isclose(P, 0.07417990022744862, rel_tol=0.0000001)

def test_ttest_P_unpaired():
    #TODO: proper check
    X = [1, 2, 3]
    Y = [1, 4, 6]
    df = len(X) + len(Y) - 2
    
    xbar, sdx = mean(X), sd(X)
    ybar, sdy = mean(Y), sd(Y)
    s = (sdx * sdx * (len(X)-1) + sdy * sdy * (len(Y)-1)) / df
    sdiff = sqrt(s * (1.0 / len(X) + 1.0 / len(Y)))
    adiff = fabs(xbar - ybar)
    
    print(sdiff, adiff)
    tval = sdiff / adiff
    print(tval)
    assert isclose(tval, 0.9380831519646861, rel_tol=0.0000001)
    
    P = ttestPDF(tval, df)
    print(P)
    assert isclose(P, 0.40131270580971734, rel_tol=0.0000001)
    
    
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
