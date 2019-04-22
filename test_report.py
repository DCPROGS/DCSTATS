import sys
import os
import pandas as pd
import socket
import datetime

import dcstats
from GUI.report import Report 

def get_sys_info():
    return ("DC-stats version: {0}".format(dcstats.__version__) +
            "Machine: {0};  System: {1};\nSystem Version: {2}".format(socket.gethostname(), sys.platform, sys.version) +
            "Date and time of analysis: " + str(datetime.datetime.now())[:19])


filename = "tests\multi_samples.xlsx"
path, fname = os.path.split(filename)
fname = os.path.splitext(fname)[0]
sysinfo = get_sys_info()
xl = pd.ExcelFile(filename)
df = xl.parse('EC50')
print(str(df.describe()))

names = df.columns.tolist()
n = len(names)

report = Report(fname, sysinfo, suffix='EC50')
report.title('Original data:', 1)
report.paragraph('Number of datasets loaded: ' + str(n))
#for fit in self.parent.fits.list:
#            self.parent.report.dataset(fit.data.title, str(fit.data))


report.outputhtml()

for i in range(n-1):
    for j in range(i+1, n):
        print('\n*****   ' + names[i] + ' versus ' + names[j] + '   *****')