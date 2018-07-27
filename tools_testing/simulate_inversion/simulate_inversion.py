#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "zhangxu"

import os
import sys
from docopt import docopt
sdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, sdir)
from produce_fa import produce_fasta
from art_produce_fq import produce_fq
from inversion_bp import inversion_bp
from merge_file import merge_file

def info_sorting(sum_info):

    ins_sum_info = "./data/inversion_info.txt"
    title = "Frequency" + "\t" + "Type" + "\t" + "Var_Type" + "\t" + "Interval" + "\t" + "Raw" + "\t" + "New" + "\n"

    with open(ins_sum_info, 'w') as fw:
        fw.write(title)

        ### parse the information in the dictionary and write in the file
        for ti, mes in sum_info.items():
            Frequency = ti
            Type = "Inversion"
            info = mes['info']
            Var_Type = info[0]
            Interval = info[1]
            Raw = info[2]
            New = info[3]
            cont = str(Frequency) + "\t" + Type + "\t" + Var_Type + "\t" + Interval + "\t" + Raw + "\t" + New + "\n"
            fw.write(cont)

def main_inversion(arguments):

    reads_length = arguments['--length']
    multiple_count = int(arguments['--count']) * (1 - float(arguments['MULTIPLE']))
    single_count = int(arguments['--count']) * float(arguments['MULTIPLE'])
    bp = arguments['--basepair']
    repeat_time = arguments['--times']

    sum_info = {}
    for ti in range(int(repeat_time)):
        raw_fasta_prefix = "raw_inversion_" + str(ti + 1)
        raw_fasta = produce_fasta(raw_fasta_prefix)
        multiple_output = "/".join(raw_fasta.split("/")[:2]) + "/multiple"
        single_output = "/".join(raw_fasta.split("/")[:2]) + "/single"
        produce_fq(raw_fasta, reads_length, multiple_count, multiple_output)
        info_record = inversion_bp(bp, raw_fasta)
        new_fasta = info_record['fasta']
        produce_fq(new_fasta, reads_length, single_count, single_output)
        files = [multiple_output, single_output]
        fq1, fq2 = merge_file(files)
        sum_info[(ti+1)] = info_record
        info_sorting(sum_info)
        ### add tools to be tested here ###

        ###################################

if __name__ == "__main__":
    usage = """
    Usage:
        simulate_inversion.py [-l=150] [-c=100000] [-b=1] [-t=1] MULTIPLE

    Testing different tool on different raw-fasta-based inversion variation

    Arguments:
        MULTIPLE        the proportion of inversed-variation fastas in all fastas

    Options:
        -h --help
        -l,--length=150         reads length of simulated fasta [default: 150]
        -c,--count=100000       number of reads/read pairs [default: 100000]
        -b,--basepair=1         the length of inversed bases [default: 1]
        -t,--times=1            the repeat time [default: 1]
    """

    arguments = docopt(usage)
    main_inversion(arguments)