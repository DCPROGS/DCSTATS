# DC Stats
Python port of David Colquhoun's Statistics Tools

Work porting to Python from original FORTRAN was begun by Remigijus Lape at UCL. This port takes advantage of the nice Tkinter implementation in macOS. 

Working out of the box on MacOS X 10.8 - 10.13 with no dependencies. Expected to work with Python version 2.7.15 (packaged with macOS) or Python 3.

Examples of how to use modules are provided in Jupyter notebooks (.ipynb files). 

To run, open the Terminal, navigate to the DC-Stats-for-Mac directory and type:

  python DC_Stats.py

You can do a randomization test on continuous or binomial data, and look at Fiellers theorem for the standard deviation of a ratio too. For continuous randomization test, information about effect size (Hedges' unbiased d and its approximate confidence interval from bootstrap) is also included in the output. 

To use data from Excel, save the two sets of values in two columns as tab-delimited text without titles.

# Projected ongoing development
This software is under development. Output is not fully tested, and therefore you should exercise caution if you plan to use the results for production / publication. 

Full Qt GUI is planned for Windows. We hope this approach will work in Linux too.  
Ultimately, we wish to include batch processing of data, and intuitive import and export.


