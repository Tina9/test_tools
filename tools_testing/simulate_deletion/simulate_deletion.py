#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__authore__ = "zhangxu"

import os
import subprocess
from docopt import docopt
from produce_fa import produce_fasta
from art_produce_fq import produce_fq
from deletion_bp import deletion_bp
from art_produce_fq import produce_fq
from merge_file import merge_file

def info_sorting(sum_info):

    del_sum_info = "./data/deletion_info.txt"
    title = "Frequency" + "\t" + "Type" + "\t" + "Var_Type" + "\t" + "Interval" + "\t" + "Raw" + "\t" + "New" + "\n"

    with open(del_sum_info, 'w') as fw:
        fw.write(title)
    
        ### parse the infomation in the dictionary and write in the file
        for ti, mes in sum_info.items():
            Frequency = ti
            Type = "Deletion"
            info = mes['info']
            Var_Type = info[0]
            Interval = info[1]
            Raw = info[2]
            New = "-"
            cont = str(Frequency) + "\t" + Type + "\t" + Var_Type + "\t" + Interval + "\t" + Raw + "\t" + New + "\n"
            fw.write(cont)

def main_function(arguments):

    reads_length = arguments['--length']
    multiple_count = int(arguments['--count']) * (1 - float(arguments['MULTIPLE']))    
    single_count = int(arguments['--count']) * float(arguments['MULTIPLE'])
    bp = arguments['--basepair']
    repeat_time = arguments['--times']

    sum_info = {}
    for ti in range(int(repeat_time)):
        raw_fasta_prefix = "raw_deletion_" + str(ti+1)
        raw_fasta = produce_fasta(raw_fasta_prefix)
        multiple_output = "/".join(raw_fasta.split("/")[:2]) + "/multiple"
        single_output = "/".join(raw_fasta.split("/")[:2]) + "/single"
        produce_fq(raw_fasta, reads_length, multiple_count, multiple_output)
        info_record = deletion_bp(bp, raw_fasta)
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
        simulate_deletion.py [-l=150] [-c=100000] [-b=1] [-t=1] MULTIPLE

    Testing different tool on different raw-fasta-based deletion variation
        
    Arguments:
        MULTIPLE        the proportion of deleted-variation fastas in all fastas
        
    Options:
        -h --help
        -l,--length=150         reads length of simulated fasta [default: 150]
        -c,--count=100000       number of reads/read pairs [default: 100000]
        -b,--basepair=1         the deleted base [default: 1] 
        -t,--times=1            the repeat time [default: 1]
    """
    
    arguments = docopt(usage)
    main_function(arguments)
    
