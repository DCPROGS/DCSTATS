#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt, fabs

import dcstats.statistics_EJ as s
from dcstats.basic_stats import mean, sd, sdm, ttestPDF

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_beta_incomplete():
    
    bi = s.incompleteBeta(0.5, 1, 2)
    assert isclose(0.75, bi, rel_tol=0.0001)
    
    try:
        from scipy.special import betainc
        spbi = betainc(1, 2, 0.5)
        assert isclose(spbi, bi, rel_tol=0.0001)
    except:
        print('scipy not available')
    
def test_mean():
    X = [1, 2, 3]
    assert mean(X) == 2
    
def test_sd():
    X = [1, 2, 3]    
    assert isclose(sd(X), 1.0, rel_tol=0.0001)
    
def test_sdm():
    X = [1, 2, 3]    
    print(sdm(X))
    assert isclose(sdm(X), 0.57735026918963, rel_tol=0.000001)
    
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
    
    
