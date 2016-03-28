import os
import re
import multiprocessing
from datetime import datetime
from glob import glob
from os.path import isfile, join, isdir
import sys
from subprocess import call
import run_parser

def parseFile(infile):
	raw_file = os.path.join(input_dir,os.path.basename(infile))
	filename = os.path.basename(os.path.splitext(infile)[0])
	output_sen = os.path.join(output_dir,filename+'_sen.dis')
	output_doc = os.path.join(output_dir,filename+'_doc.dis')
	if not (os.path.exists(output_sen) and os.path.exists(output_doc)):
		print filename, "starts at", format(datetime.now()) , "in process ", os.getpid()
		#print "Start time: " + format(datetime.now())
		run_parser.main(raw_file, output_dir)

def main(input_dir, output_dir):
	files = sorted(glob(os.path.join(input_dir,'*.txt')))
	print "Number of cores available:", multiprocessing.cpu_count()
	pool = multiprocessing.Pool()
	pool.map(parseFile, files)
	pool.close()
	pool.join()

# Returns usage specification.
def usage():
    return 'Usage: python run_multiparser <input directory> <output directory>'
	
	
if __name__ == '__main__':
    # ensure number of arguments is correct
	if len(sys.argv) != 3:
		sys.exit('Error: incorrect number of arguments\n' + usage())
    # input_dir must be a directory
	input_dir = sys.argv[1]
	if not isdir(input_dir):
		sys.exit('Error: ' + input_dir + ' is not a valid directory')
    # output_dir must be a directory
	output_dir = sys.argv[2]
	if not isdir(output_dir):
		sys.exit('Error: ' + output_dir + ' is not a valid directory')
    # execute the script
	start_time = datetime.now()
	print "***************** Directory start time: " + format(start_time) + " ****************"
	main(input_dir, output_dir)
	end_time = datetime.now()
	print "***************** Directory end time: " + format(end_time) + " ****************"
	print "----------------- Directory time cost: [[" + format(end_time - start_time) + "]] -------------"
