#!/usr/bin/env python
import argparse,os,sys
from subprocess import Popen, PIPE, call
from collections import Counter
import datetime

import tacc_stats.analysis.exam.tests as tests
import tacc_stats.analysis.plot.plots as plots
import tacc_stats.analysis.gen.tspl_utils as tspl_utils

def main():

    parser = argparse.ArgumentParser(description='Plot list of jobs')
    parser.add_argument('-p', help='Set number of processes',
                        nargs=1, type=int, default=[1])
    parser.add_argument('-files', help='Files to plot',
                        nargs='?', type=str)
    parser.add_argument('-mode', help='Style of plot: lines, percentile',
                        nargs=1, type=str,default=['lines'])
    parser.add_argument('-header', help='Header of plot',
                        nargs=1, type=str,default=[''])
    parser.add_argument('-prefix', help='Prefix of plot name',
                        nargs=1, type=str,default=[''])
    parser.add_argument('-plot', help='Plot type to generate',
                        nargs='?', type=str)
    parser.add_argument('-full', help='Do not aggregate over node',action="store_true")
    parser.add_argument('-o', help='Output directory',
                        nargs=1, type=str, default=['.'], metavar='output_dir')
    parser.add_argument('-wide', help='Set wide plot format',
                        action="store_true")

    args=parser.parse_args()
    print args
    import inspect
    for name, obj in inspect.getmembers(plots):
        if hasattr(obj,"__bases__") and plots.Plot in obj.__bases__:            
            if args.plot in obj.__name__:
                plot = obj(processes=args.p[0],mode=args.mode[0], 
                           header=args.header[0],
                           prefix=args.prefix[0],outdir=args.o[0],
                           aggregate=(not args.full),save=True)

                filelist=tspl_utils.getfilelist(args.files)
                for f in filelist:
                    plot.plot(f)

if __name__ == '__main__':
    main()