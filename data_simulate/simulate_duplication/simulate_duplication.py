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
from duplication_bp import duplication_bp
from merge_file import merge_file

def info_sorting(sum_info):

    dup_sum_info = "./data/duplication_info.txt"
    title = "Frequency" + "\t" + "Type" + "\t" + "Var_Type" + "\t" + "Interval" + "\t" + "Raw" + "\t" + "New" + "\t" + "fasta" + "\t" + "fq1" + "\t" + "fq2" + "\n"

    with open(dup_sum_info, 'w') as fw:
        fw.write(title)

        ### parse the information in the dictionary and write in the file
        for ti, mes in sum_info.items():
            Frequency = ti
            Type = "Duplication"
            info = mes['info']
            Var_Type = info[0]
            Interval = info[1]
            Raw = info[2]
            New = info[3]
            fasta = mes['raw_fasta']
            fq1 = mes['fq1']
            fq2 = mes['fq2']
            cont = str(Frequency) + "\t" + Type + "\t" + Var_Type + "\t" + Interval + "\t" + Raw + "\t" + New + "\t" + fasta + "\t" + fq1 + "\t" + fq2 + "\n"
            fw.write(cont)

    return dup_sum_info

def main_duplication(reads_length, multiple_count, single_count, bp, repeat_time, copy_number):

    sum_info = {}
    for ti in range(int(repeat_time)):
        raw_fasta_prefix = "raw_duplication_" + str(ti + 1) + "_"+ str(bp) + "bp"
        raw_fasta = produce_fasta(raw_fasta_prefix)
        multiple_output = "/".join(raw_fasta.split("/")[:2]) + "/multiple" + '_' + str(ti+1) + '_dup_' + str(bp) + "bp" + "_"
        single_output = "/".join(raw_fasta.split("/")[:2]) + "/single" + '_' + str(ti+1) + '_dup_' + str(bp) + "bp" + "_"
        produce_fq(raw_fasta, reads_length, multiple_count, multiple_output)
        info_record = duplication_bp(bp, raw_fasta, copy_number)
        new_fasta = info_record['fasta']
        produce_fq(new_fasta, reads_length, single_count, single_output)
        files = [multiple_output, single_output]
        fq1, fq2 = merge_file(files)
        info_record['fq1'] = fq1
        info_record['fq2'] = fq2
        info_record['raw_fasta'] = raw_fasta
        sum_info[(ti+1)] = info_record
        dup_sum_info = info_sorting(sum_info)
        ### add tools to be tested here ###

        ###################################

    return sum_info, dup_sum_info

def parse_parameters(arguments):

    reads_length = arguments['--length']
    multiple_count = int(arguments['--count']) * (1 - float(arguments['MULTIPLE']))
    single_count = int(arguments['--count']) * float(arguments['MULTIPLE'])
    bp = arguments['--basepair']
    repeat_time = arguments['--times']
    copy_number = arguments['--copys']
    
    ###### use the function to test tools ######
    main_duplication(reads_length, multiple_count, single_count, bp, repeat_time, copy_number)

if __name__ == "__main__":
    usage = """
    Usage:
        simulate_duplication.py [-l=150] [-c=100000] [-b=1] [-p=1] [-t=1] MULTIPLE

    Testing different tool on different raw-fasta-based duplication variation

    Arguments:
        MULTIPLE        the proportion of duplicated-variation fastas in all fastas

    Options:
        -h --help
        -l,--length=150         reads length of simulated fasta [default: 150]
        -c,--count=100000       number of reads/read pairs [default: 100000]
        -b,--basepair=1         the length of duplicated bases [default: 1]
        -p,--copys=1            the copy number [default: 1] 
        -t,--times=1            the repeat time [default: 1]
    """

    arguments = docopt(usage)
    parse_parameters(arguments)
