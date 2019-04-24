import sys
import os
import pandas as pd
import socket
import datetime
import matplotlib.pyplot as plt

import dcstats
from dcstats import rantest
from dcstats.ratio import Ratio
from dcstats.difference import Difference
from GUI.report import Report 
from dcstats.twosamples import TwoSamples

def get_sys_info():
    return ("DC-stats version: {0}".format(dcstats.__version__) +
            "Machine: {0};  System: {1};\nSystem Version: {2}".format(socket.gethostname(), sys.platform, sys.version) +
            "Date and time of analysis: " + str(datetime.datetime.now())[:19])


filename = "tests\multi_samples.xlsx"
path, fname = os.path.split(filename)
fname = os.path.splitext(fname)[0]
fname = fname +'_EC50'

print(fname)
sysinfo = get_sys_info()
xl = pd.ExcelFile(filename)
df = xl.parse('EC50')
print(str(df.describe()))

new_path = os.path.join(path, "temp")
if not os.path.exists(new_path):
    os.mkdir(new_path)
os.chdir(new_path)

names = df.columns.tolist()
n = len(names)

nran = 10000

report = Report(fname, sysinfo)
report.title('Original data:', 1)
report.paragraph('Number of samples loaded: ' + str(n))
#for fit in self.parent.fits.list:
#            self.parent.report.dataset(fit.data.title, str(fit.data))

for i in range(n-1):
    for j in range(i+1, n):
        df2 = df.iloc[:, [i, j]]
        A = df.iloc[:, i].dropna().values.tolist()
        B = df.iloc[:, j].dropna().values.tolist()

        report.title('\n\n********************', 1)
        report.dataset('\n*****   ' + names[i] + ' versus ' + names[j] + '   *****', 
                str(df2.describe()))
        twosamples = TwoSamples(df2, runs=nran)
        report.paragraph(str(twosamples.describe_data()))
        #print(str(twosamples.describe_data()))
        fig = twosamples.plot_boxplot()
        fname_boxplot = fname  + '_boxplot_' + names[i] + '_' + names[j] + '.svg'
        fig.savefig(fname_boxplot)
        report.image(fname_boxplot)
        plt.close(fig)

        #fig = twosamples.plot_bootstrapped_distributions()
        #fname_samples_boot = fname  + '_boot_samples_' + names[i] + '_' + names[j] + '.svg'
        #fig.savefig(fname_samples_boot)
        #report.image(fname_samples_boot)
        #plt.close(fig)

        #fig = twosamples.plot_qq_plots()
        #fname_samples_boot = fname  + '_qq_' + names[i] + '_' + names[j] + '.svg'
        #fig.savefig(fname_samples_boot)
        #report.image(fname_samples_boot)
        #plt.close(fig)

        rnt = rantest.RantestContinuous(A, B, False)
        rnt.run_rantest(nran)
        report.paragraph(str(rnt))
        fig = rnt.plot_rantest()
        fname_boxplot = fname  + '_rantest_' + names[i] + '_' + names[j] + '.svg'
        fig.savefig(fname_boxplot)
        report.image(fname_boxplot)
        plt.close(fig)

        report.title('\n Ratio:', 1)
        ratio = Ratio(A, B)
        ratio.run_bootstrap(nran)
        report.paragraph(str(ratio))
        report.title('\n Reciprocal:', 1)
        recip = Ratio(B, A)
        recip.run_bootstrap(nran)
        report.paragraph(str(recip))
        fig = ratio.plot_bootstrap()
        fname_ratio = fname  + '_ratio_boot_' + names[i] + '_' + names[j] + '.svg'
        fig.savefig(fname_ratio)
        report.image(fname_ratio)
        plt.close(fig)

        report.title('\n Difference:', 1)
        diff = Difference(A, B)
        diff.run_bootstrap(nran)
        report.paragraph(str(diff))
        fig = diff.plot_bootstrap()
        fname_diff = fname  + '_diff_boot_' + names[i] + '_' + names[j] + '.svg'
        fig.savefig(fname_diff)
        report.image(fname_diff)
        plt.close(fig)

report.outputhtml()
