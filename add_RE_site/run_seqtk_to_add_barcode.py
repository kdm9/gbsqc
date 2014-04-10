#!/usr/bin/env python
import csv
import docopt
from copy import deepcopy
from subprocess import Popen
import os
import re
from os import path
import multiprocessing as mp

CLI_OPTS = """
USAGE:
    barcodise.py [-p PATTERN -o OUTDIR -i INDIR] -k KEYFILE

OPTIONS:
    -k KEYFILE      The key file, in Aaron's format
    -p PATTERN      Process all files matching pattern.
                        [Default: sample_(\w{2,3})-.+-clipped_filtered\\.fq]
    -i INDIR        Input dir
                        [Default:  .]
    -o OUTDIR       Output dir
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


def run_seqtk(args):
    args = list(args)
    args.insert(0, "/home/kevin/bin/seqtk")
    args.insert(1, "seq")
    #ofh = open(args.pop(), "w")
    print " ".join(args)
    #proc = Popen(args, stdout=ofh)
    #proc.wait()
    #ofh.close()


def main(opts):
    kd = get_key_dict(opts["-k"])
    fqfiles = get_fq_files(opts["-i"], opts["-p"])
    seqtk_calls = []
    for fqfile in fqfiles:
        match = re.search(opts["-p"], fqfile)
        if not match:
            continue
        sample = match.group(1)
        if "-o" in opts and path.exists(opts["-o"]):
            out_file = path.join(opts["-o"], path.basename(fqfile))
        else:
            in_f, in_ext = path.splitext(fqfile)
            out_file = "_".join((in_f, ".".join(("barcoded", in_ext))))
        seqtk_calls.append((
            fqfile,
            "-b",
            kd[sample]["barcode"],
            "-B",
            "I" * len(kd[sample]["barcode"]),
            ">",
            out_file))
    pool = mp.Pool(mp.cpu_count() - 1)
    map(run_seqtk, seqtk_calls)
    pool.close()
    pool.join()

if __name__ == "__main__":
    opts = docopt.docopt(CLI_OPTS)
    main(opts)


