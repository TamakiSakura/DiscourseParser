# author: Jordon Johnson

import os
import sys
import glob
from datetime import datetime
from subprocess import call
import Discourse_Parser
from os.path import isfile, join, isdir





def main(raw_file, output_dir):
	start_time = datetime.now()
	TMP_SEGMENTED_FILE = "seg_"
	TMP_EXT= ".txt"
	TMP_SEGMENTED_FILE = TMP_SEGMENTED_FILE + os.path.basename(raw_file)
	temp_file = open(join(output_dir, TMP_SEGMENTED_FILE), "w")
	print "Running segmenter... ",
	call(["python", "Discourse_Segmenter.py", raw_file], stdout=temp_file)
	seg_time = datetime.now()
	print format(seg_time - start_time)
	print "Running parser...    ",
	Discourse_Parser.do_parse(join(output_dir, TMP_SEGMENTED_FILE))
	temp_file.close()
	parse_time = datetime.now()
	print format(parse_time - seg_time)
	#print("Copying output files...")
	#call(["cp", "-t", output_dir] + glob.glob("tmp_*"))
	call(["cp", "-t", output_dir] + glob.glob("tmp_sen.dis"))
	call(["cp", "-t", output_dir] + glob.glob("tmp_doc.dis"))
	end_time = datetime.now()
	print "Done. End time:", format(end_time), ". Total time cost: [", format(end_time - start_time), "]"


# Returns usage specification.
def usage():
    return 'Usage: python run_parser <file> <output directory>'


if __name__ == '__main__':
    # ensure number of arguments is correct
    if len(sys.argv) != 3:
        sys.exit('Error: incorrect number of arguments\n' + usage())
    # raw_file must be a file
    raw_file = sys.argv[1]
    if not isfile(raw_file):
        sys.exit('Error: ' + raw_file + ' is not a valid file')
    # output_dir must be a directory
    output_dir = sys.argv[2]
    if not isdir(output_dir):
        sys.exit('Error: ' + output_dir + ' is not a valid directory')
    # execute the script
    main(raw_file, output_dir)
