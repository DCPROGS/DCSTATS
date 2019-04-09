#!/usr/bin python
"""ratio.py -- calculate statistics for a ratio of two means."""

import math
import numpy as np

__author__="remis"
__date__ ="$09-Apr-2019 13:48:16$"

class Ratio:
    def __init__(self, S1, S2):
        """ 
        Parameters
        ----------
        S1 : observations in first trial, numpy array or list
        S2 : observations in second trial, numpy array or list
        """   
        self.A = S1
        self.B = S2
     
    def ratio(self):
        return np.mean(self.A) / np.mean(self.B)

    def reciprocal(self):
        return np.mean(self.B) / np.mean(self.A)

    def __repr__(self):
        return ('\nRatio = {0:.3e}; (reciprocal = {0:.3e}) '.
            format(self.ratio(), self.reciprocal()))

