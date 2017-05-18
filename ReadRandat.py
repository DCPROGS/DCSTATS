import os, sys
import csv
if sys.version_info[0] < 3:
    import tkFileDialog
else:
    from tkinter import filedialog as tkFileDialog

__author__="Remijigus Lape and Andrew Plested"
__date__ ="$01-Dec-2009 16:16:16$"

#functions file_write and traces_into_lines are not used
#in file_write, os.linesep is used now to write the end-of-line
# Jargon: Traces are lists of floating point numbers
#           Lines are strings of tab-delimited floating point numbers
#
#Note: this module is unsafe and not robust to bad input.

def read_Data(file_type):
    """"Asks for a tab delimited text file or excel tab-delim to use in randomization test.
    file_type :string, can be txt or excel
    """

    data_file_name = tkFileDialog.askopenfilename()

    #Convert file into lines of tab delimited text
    lines_of_file = file_read(data_file_name, file_type)

    # Imagine taking a header here, with data titles?

    #Make lines into lists of floating point numbers
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

    return in_data, data_file_name


def file_read (data_file_name, file_type='txt'):
	"""Strip lines of ASCII text from file"""
	print ('Reading',data_file_name,'....')           #silence this output
	
	if file_type == 'txt':

		lines = []
		f=open(data_file_name, 'rU')
		for line in f:
				lines.append(line)
		f.close()							#close the file

		#eol = os.linesep                 # not required, probably can remove import of os module
		#lines = block_lines.splitlines() 	#divide into lines at carriage rtns, should be platform independent
		lines_of_file=[]
		
		for line in lines:
			values=line.split('\t')					#divide lines into values at tabs
			lines_of_file.append(values)

	elif file_type == 'excel':

		lines_of_file = []

		#from http://stackoverflow.com/questions/11059390/parsing-a-tab-separated-file-in-python

		with open(data_file_name, "rU") as tsv:
			for line in csv.reader(tsv, dialect="excel-tab"):
				lines_of_file.append(line)
		
	return lines_of_file

def file_write (file,data):
	"""Write lines of data to ASCII file"""
	### NOT USED
	f=open(file, "w")
	for each_line in data:
		joined_line = '\t'.join(each_line)  	# \t for tab
		f.write(joined_line+'\n') 					# Write the line.
		#f.write(os.linesep) 				# write a carriage return what a nasty hack! obsolete due to change in last line
	f.close()
	return

def lines_into_traces (lines):
	"""Convert a list of split ASCII text lines into traces (a list of lists of floats)"""
	
	traces = []
	num_of_traces = len(lines[0])			#work out how many traces from the no of columns

	## make an empty list
	for i in range(num_of_traces):
		traces.append([])

	## transpose lines into traces made from columns
	for line in lines:
		print (line)
		for i in range (num_of_traces):
			#NEW AP
			print (line[i])
			try:
				traces[i].append (float(line[i]))
			except:
				#element is empty or not a number, so skip
				continue
	return traces


if __name__ == "__main__":
    scnFile = tkFileDialog.askopenfilename(filetypes=ftypes)
    if os.path.exists(scnFile):
        HeaderList = readHeader(scnFile)
    else:
        print ('file not found')


