#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas

from dcstats.rantest import RantestBinomial
from dcstats.rantest import RantestContinuous
#from test_statistics import isclose

def test_regression_rantest_continuos():
    # Samples from treatment T1 and T2
    T1 = [100, 108, 119, 127, 132, 135, 136] #, 164]
    T2 = [122, 130, 138, 142, 152, 154, 176]
    df = pandas.DataFrame({'Sample1':T1, 'Sample2':T2})
    rnt = RantestContinuous(df, True)    
    rnt.run_rantest(5000)
    assert (rnt.p2tail == 0.018)
    assert (rnt.n2tail == 90)
    rnt = RantestContinuous(df, False)
    rnt.run_rantest(5000)    
    assert (rnt.p2tail == 0.0178)
    assert (rnt.n2tail == 89)
   
def test_regression_rantest_binomial():
    rnt = RantestBinomial(3, 4, 4, 5)
    rnt.run_rantest(5000)
    assert (rnt.ng1/rnt.nran == 0.718)
 