#! /usr/bin/python

from dcstats.statistics_EJ import InverseStudentT
import unittest as ut

class Test (ut.TestCase):
    
    def testT(self):
        table5 = { 0.9 : 1.476,  }
        
        dfs = (5, 10, 120, 1000)
        for i in range (100, 200, 1):
            P = float(i) / 200
            for df in dfs:
                t = InverseStudentT(df, P)
                #print(df, P, t)
                if P in table5 and df == 5:
                    print (df, P, table5[P], t)
                    self.assertAlmostEqual(table5[P], t, places=3, msg=None, delta=None)



if __name__ == "__main__":

    ut.main()
