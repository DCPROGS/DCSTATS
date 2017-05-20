#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

from fieller import Fieller
import statistics_EJ as s

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
    
    assert math.isclose(flr.ratio, 2.00000, rel_tol=0.0001)
    assert math.isclose(flr.g, 0.268164, rel_tol=0.001)
    assert math.isclose(flr.clower, 1.051413, rel_tol=0.0001)
    assert math.isclose(flr.cupper, 4.414296, rel_tol=0.0001)
    assert math.isclose(flr.dlow, -0.948587, rel_tol=0.0001)
    assert math.isclose(flr.dhi, 2.414296, rel_tol=0.0001)
    assert math.isclose(flr.appsd, 0.714286, rel_tol=0.0001)
    assert math.isclose(flr.cvr, 35.714286, rel_tol=0.0001)
    assert math.isclose(flr.applo, 0.705385, rel_tol=0.0001)
    assert math.isclose(flr.apphi, 3.294615, rel_tol=0.0001)
    #assert 0 == 1