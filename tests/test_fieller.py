#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dcstats.fieller import Fieller
import dcstats.statistics_EJ as s

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def test_zero_input():
    # a, b, sa, sb, r, tval
    f = Fieller(0, 1, 0, 0, 0, 0)

    expected_output = {
        'ratio' : 0.0,
        'clower': 0.0,
        'cupper': 0.0,
        'dlow'  : 0.0,
        'dhi'   : 0.0,
        'appsd' : 0.0,
        'applo' : 0.0,
        'apphi' : 0.0,
        'cvr'   : 0.0}
        
    for key in expected_output :
        fieller_output = vars(f)[key]
        expected = expected_output[key]
        assert fieller_output == expected

def test_regression_fieller():
    a, b = 14, 7 # Nominator and denominator
    sa, sb = 3, 2 # SD of nominator and denominator
    r = 0 # Correlation coefficient (a,b)
    alpha = 0.05 # alpha
    n = 12 # Total number of observations na + nb
    
    df = n - 2
    two_tail = 1 - float(alpha)
    tval = s.InverseStudentT(int(df), two_tail )
    
    flr = Fieller(a, b, sa, sb, r, tval)
    print(flr)
    
    assert isclose(flr.ratio, 2.00000, rel_tol=0.0001)
    assert isclose(flr.g, 0.268164, rel_tol=0.001)
    assert isclose(flr.clower, 1.051413, rel_tol=0.0001)
    assert isclose(flr.cupper, 4.414296, rel_tol=0.0001)
    assert isclose(flr.dlow, -0.948587, rel_tol=0.0001)
    assert isclose(flr.dhi, 2.414296, rel_tol=0.0001)
    assert isclose(flr.appsd, 0.714286, rel_tol=0.0001)
    assert isclose(flr.cvr, 35.714286, rel_tol=0.0001)
    assert isclose(flr.applo, 0.705385, rel_tol=0.0001)
    assert isclose(flr.apphi, 3.294615, rel_tol=0.0001)
    #assert 0 == 1