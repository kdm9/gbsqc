#!/usr/bin/env python
import csv
import docopt
from copy import deepcopy
import os
import re
from os import path

CLI_OPTS = """
USAGE:
    barcodise.py [-p PATTERN -o OUTDIR -i INDIR -s SEQTK_PATH] -k KEYFILE

OPTIONS:
    -k KEYFILE      The key file, in Aaron's format
    -p PATTERN      Process all files matching pattern.
                        [Default: sample_(\w{2,3})-.+-clipped_filtered\\.fq]
    -i INDIR        Input dir
                        [Default:  .]
    -o OUTDIR       Output dir
    -s SEQTK_PATH   Path to seqtk script [Default: /usr/local/bin/seqtk]
"""

def get_key_dict(fn):
    fh = open(fn)
    sample_keys = csv.DictReader(fh, delimiter="\t")
    key_dict = {}
    for sample_key in sample_keys:
        if sample_key["read"] == "1":
            sample = sample_key["sample"]
            sample_dict = deepcopy(sample_key)
            sample_dict.pop("sample")
            key_dict[sample] = sample_dict
    return key_dict


def get_fq_files(dir, pattern):
    fqfiles = []
    for this_dir, sub, files in os.walk(dir):
        for file in files:
            match = re.search(pattern, file)
            if match is not None:
                fqfiles.append(path.join(this_dir, file))
    return fqfiles


def main(opts):
    kd = get_key_dict(opts["-k"])
    fqfiles = get_fq_files(opts["-i"], opts["-p"])
    seqtk_calls = []
    for fqfile in fqfiles:
        match = re.search(opts["-p"], fqfile)
        if not match:
            continue
        sample = match.group(1)
        if "-o" in opts and opts['-o'] is not None and path.exists(opts["-o"]):
            out_file = path.join(opts["-o"], path.basename(fqfile))
        else:
            in_f, in_ext = path.splitext(fqfile)
            out_file = in_f +  ".barcoded" + in_ext
        print opts['-s'], "seq", fqfile, "-b", kd[sample]["barcode"], "-B", \
                "I" * len(kd[sample]["barcode"]), ">", out_file


if __name__ == "__main__":
    opts = docopt.docopt(CLI_OPTS)
    main(opts)


