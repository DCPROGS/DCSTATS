import os
import tkFileDialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__author__="remis, and andrew"
__date__ ="$01-Dec-2009 16:16:16$"

#functions file_write and traces_into_lines are not used
#in file_write, os.linesep is used now to write the end-of-line
# Jargon: Traces are lists of floating point numbers
#           Lines are strings of tab-delimited floating point numbers

def read_Data(parent):
    """"Asks for a tab delimited text file to use in randomization test."""


    file = QFileDialog.getOpenFileName(parent,
     "Open Data File...", "", "Text Data Files (*.txt)")

    #Convert file into lines of tab delimited text
    lines_of_file = file_read(file)

    # Imagine taking a header here, with data titles

    #Make lines into vertical lists of floating point numbers
    datalines = lines_into_traces(lines_of_file)
    data1 = datalines[0]
    data2 = datalines[1]

    n1 = len(data1)
    n2 = len(data2)
    nset = 1    # number of data sets

    #standard construction of in_data
    in_data = []
    in_data.append(nset)
    for j in range(0, nset):
        in_data.append(n1)
        in_data.append(n2)
        titled = 'Set'
        titlex = 'Sample 1'
        titley = 'Sample 2'
        in_data.append(titled)
        in_data.append(titlex)
        in_data.append(titley)
        in_data.append(data1)
        in_data.append(data2)

    return in_data, file

def file_read (file):
	"""Strip lines of ASCII text from file"""
	#print 'Reading',file,'....',           #silence this output
	f=open(file, 'r')
	block_lines = f.readline()
	f.close()							#close the file

	#eol = os.linesep                           # not required, probably can remove import of os module
	lines_of_file = block_lines.splitlines() 	#divide into lines at carriage rtns, should be platform independent

	return lines_of_file

def file_write (file,data):
	"""Write lines of data to ASCII file"""
	f=open(file, "w")
	for each_line in data:
		joined_line = '\t'.join(each_line)  	# \t for tab
		f.write(joined_line+'\n') 					# Write the line.
		#f.write(os.linesep) 				# write a carriage return what a nasty hack! obsolete due to change in last line
	f.close()
	return

def lines_into_traces (lines):
	"""Convert a list of ASCII text lines into traces (a list of lists of floats)"""
	
	split_lines=[]
	for line in lines:
		values=line.split('\t')					#divide lines into values at tabs
		split_lines.append(values)

	traces = []
	num_of_traces = len(split_lines[0])			#work out how many traces from the no of columns

	## make an empty list
	for i in range(num_of_traces):
		traces.append([])

	## transpose lines into traces made from columns
	for line in split_lines:
		for i in range (num_of_traces):
			traces[i].append (float(line[i]))

	return traces

def traces_into_lines (traces):
	"""Convert traces (a list of lists of floats) into a list of ASCII text lines"""

	lines_of_output=len(traces[0])

	## make an empty list
	lines = []
	for i in range(lines_of_output):
		lines.append([])

	## transpose the traces into lines
	for point in range(0,lines_of_output):
		for trace in traces:
			lines[point].append(str(trace[point]))

	return lines

if __name__ == "__main__":
    scnFile = tkFileDialog.askopenfilename(filetypes=ftypes)
    if os.path.exists(scnFile):
        HeaderList = readHeader(scnFile)
    else:
        print 'file not found'


