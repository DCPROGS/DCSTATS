#! /usr/bin/python

from Fieller import Fieller
import nose

# a, b, sa, sb, r, tval
test_input = [0, 1, 0, 0, 0, 0]
    
expected_output = {
    'ratio' : 0,
    'clower': 0,
    'cupper': 0,
    'dlow'  : 0,
    'dhi'   : 0,
    'appsd' : 0,
    'applo' : 0,
    'apphi' : 0,
    'cvr'   : 0
            }

test_pair = [test_input, expected_output]

test_sets = [test_pair]

for set in test_sets:
    a, b, sa, sb, r, tval = set[0]
    expected_results = set[1]

    f = Fieller(a, b, sa, sb, r, tval)

    for key in expected_results :
        fieller_output = f.dict[key]
        expected = expected_results[key]
        assert fieller_output == expected



