# DC Stats for Mac
macOS version of David Colquhoun's Statistiscs Tools, written in Python

All of the work porting to Python from original FORTRAN was done by Remigijus Lape at UCL. This port takes advantage of the nice Tkinter implementation in macOS.

Working out of the box on MacOS X 10.8 - 10.12 with no dependencies. Expected to work with Python version 2.7.10 (packaged with macOS) or Python 3.

To run, open the Terminal, navigate to the DC-Stats-for-Mac directory and type:

  python DC_Stats.py

You can do a randomization test on continuous or binomial data, and look at Fiellers theorem for the standard deviation of a ratio too. For continuous randomization test, rudimentary information about effect size (Hedges' unbiased d and its approximate confidence interval from bootstrap) is also included in the output. 

To use data from Excel, save it in two columns as tab-delimited text.

This software is under development. Output is not fully tested, and therefore you should exercise caution if you plan to use the results for production / publication. 
