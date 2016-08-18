# author: Jordon Johnson


import sys
import glob
from subprocess import call
import Discourse_Parser_wProbs
from os.path import isfile, join, isdir
from os import makedirs


TMP_SEGMENTED_FILE = "temp_segmented_file.txt"


def parse(raw_file, output_dir):
    # create output_dir if it is not a valid directory
    if not isdir(output_dir):
        makedirs(output_dir)
    print("Parsing " + raw_file + ":")
    temp_file = open(join(output_dir, TMP_SEGMENTED_FILE), "w")
    print("  Running Discourse Segmenter...")
    call(["python", "Discourse_Segmenter.py", raw_file], stdout=temp_file)
    print("  Running Discourse Parser...")
    Discourse_Parser_wProbs.do_parse(join(output_dir, TMP_SEGMENTED_FILE))
    print("  Copying output files to " + output_dir + " ...")
    call(["cp", "-t", output_dir] + glob.glob("tmp_*"))
    print("  Done.")


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
    # output_dir
    output_dir = sys.argv[2]
    # execute the script
    parse(raw_file, output_dir)
