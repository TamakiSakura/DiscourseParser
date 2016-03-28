import os
import re
import multiprocessing
from datetime import datetime
from glob import glob
from os.path import isfile, join, isdir
import sys
import traceback
from subprocess import call
import run_parser

def parseFile(infile):
	raw_file = os.path.abspath(infile)
	filename = os.path.basename(os.path.splitext(infile)[0])
	group = filename.split("_")
	if(len(group)>1):
		group = group[1][:2]
	output_subdir = os.path.join(output_dir, group)
	#if(not os.path.isdir(output_subdir)):
	#	os.mkdir(output_subdir)
		
	output_sen = os.path.join(output_subdir,filename+'_sen.dis')
	output_doc = os.path.join(output_subdir,filename+'_doc.dis')
	isParsed = os.path.isfile(output_sen) and os.path.isfile(output_doc)
	isBeingParsed = os.path.isfile("temp/"+filename+"_tmp.tok")
	isSkipped = os.path.isfile("error/"+filename+".err")
	isSmall = os.path.getsize(raw_file) < 3000
	if (not isParsed) and (not isBeingParsed) and (not isSkipped) and isSmall:
		print filename, "starts at", format(datetime.now()) , "in process ", os.getpid()
		#print "Start time: " + format(datetime.now())
		try:
			run_parser.main(raw_file, output_subdir)
		except KeyboardInterrupt:
			print "\nKeyboard Interruption\n"	
			pool.close()
			sys.exit()
		except (Warning, Exception, StandardError):
			f = open("error/"+filename+".err",'a')
			err_msg = filename + " aborted at " + format(datetime.now())+ "\n"
			f.write(err_msg)
			traceback.print_exc(file = f)
			f.flush()
			f.close()
			call(["cp", "-t", "error/", raw_file]) 
			print err_msg
			traceback.print_exc()

def main(input_dir, output_dir):
	files = sorted(glob(os.path.join(input_dir,'*/*.txt')))
	print "Number of cores available:", multiprocessing.cpu_count()
	for i in range(0, 25):
		serial = str(i)
		if i < 10:
			serial = '0' + serial
		subdir = os.path.join(output_dir, serial)
		if not os.path.isdir(subdir):
			os.mkdir(subdir)	
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
