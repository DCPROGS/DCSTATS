#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import statistics_EJ as s
from rantest import Rantest
 

def test_beta_incomplete():
    
    try:
        from scipy.special import betainc
        bi = betainc(1, 2, 0.5)
        print('scipy bi= ', bi)
    except:
        print('scipy not available')
    
    rnt = Rantest()
    bi1 = rnt.betai(1, 2, 0.5)
    print('rantest bi1= ', bi1)
    
    bi2 = s.incompleteBeta(0.5, 1, 2)
    print('statistics_EJ bi2= ', bi2)
    
    assert bi1 == bi2
    
    
