#! /usr/bin/env python2
#
# A combinator of SAT solvers.
#
# Reads a sequence of SAT solvers,
# and an instance file. Solves the
# instances with the respective Solvers.
#
import argparse
import linecache
import os
from subprocess import call

SOLVERS_DIR = 'solvers/'

parser = argparse.ArgumentParser()
parser.add_argument('--solver-config', nargs = '+',
    dest = 'config', metavar = 'c', 
    help = 'A sequence of integers specifying a solver sequence.')
parser.add_argument('--instance-file',
    dest = 'file', metavar = 'f',
    required = True,
    help = 'A file containing a subset of instances to solve.')
parser.add_argument('--single-solve',
    dest = 'single',
    action = 'store_true',
    help = 'Solves a single instance with a given solver.')
parser.add_argument('--target-instance',
    dest = 'target', metavar = 't',
    help = 'The instance to solve. (only when --single-solve is passed)')
parser.add_argument('--select-solver',
    dest = 'selected', metavar = 's',
    help = 'The solver to be used. (only when --single-solver is passed)')
parser.add_argument('--benchmark',
    dest = 'benchmark', metavar = 'b',
    required = True,
    help = 'The directory with all instances to solve.')
parser.add_argument('--solve-all',
    dest = 'solve_all',
    action = 'store_true',
    help = 'Solves all instances with a given solver.')
parser.set_defaults(single=False)
parser.set_defaults(solve_all=False)

def ccanr_glucose(filename):

    cmd = SOLVERS_DIR + 'CCAnrglucose/CCAnr+glucose.sh '
    instance = filename
    args = ' 1 1000'
    #print cmd + instance + args
    #call(cmd + instance + args, shell=True)
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def glueSplit(filename):

    cmd = SOLVERS_DIR + 'glueSplit/glueSplit_clasp '
    instance = filename
    args = ''
    #print cmd + instance + args
    #call(cmd + instance + args, shell=True)
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def lingeling(filename):

    cmd = SOLVERS_DIR + 'Lingeling/lingeling -v '
    instance = filename
    args = ''
    #print cmd + instance + args
    #call(cmd + instance + args, shell=True)
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def lingeling_druplig(filename):

    cmd = SOLVERS_DIR + 'Lingeling/lingeling -v --druplig '
    instance = filename
    args = ''
    #print cmd + instance + args
    #call(cmd + instance + args, shell=True)
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def riss(filename):

    cmd = SOLVERS_DIR + 'Riss/blackbox.sh '
    instance = filename
    args = ' .'
    #print cmd + instance + args
    #call(cmd + instance + args, shell=True)
    call(cmd + instance + args, stderr=open(os.devnull, 'wb'), 
        stdout=open(os.devnull, 'wb'), shell=True)
    return

def sparrow(filename):

    cmd = SOLVERS_DIR + 'Sparrow/SparrowToRiss.sh '
    instance = filename
    args = ' 1 .'
    #print cmd + instance + args
    #call(cmd + instance + args, shell=True)
    call(cmd + instance + args, stderr=open(os.devnull, 'wb'),
        stdout=open(os.devnull, 'wb'), shell=True)
    return

args = parser.parse_args()

single_solve = args.single
solve_all = args.solve_all
INSTANCES_DIR = args.benchmark

if single_solve:

    target = args.target
    selected = args.selected
    line = linecache.getline(args.file, int(target)).rstrip()

    if (selected == '1'):
        ccanr_glucose(INSTANCES_DIR + line)
    elif (selected == '2'):
        glueSplit(INSTANCES_DIR + line)
    elif (selected == '3'):
        lingeling(INSTANCES_DIR + line)
    elif (selected == '4'):
        lingeling_druplig(INSTANCES_DIR + line)
    elif (selected == '5'):
        riss(INSTANCES_DIR + line)
    elif (selected == '6'):
        sparrow(INSTANCES_DIR + line)
    else:
        print 'ERROR: INVALID SOLVER ID!'

    linecache.clearcache()

elif solve_all:

    selected = args.selected

    instance_file = open(args.file, 'r')
    line = instance_file.readline().rstrip()            

    while line != '':

        if (selected == '1'):
            ccanr_glucose(INSTANCES_DIR + line)
        elif (selected == '2'):
            glueSplit(INSTANCES_DIR + line)
        elif (selected == '3'):
            lingeling(INSTANCES_DIR + line)
        elif (selected == '4'):
            lingeling_druplig(INSTANCES_DIR + line)
        elif (selected == '5'):
            riss(INSTANCES_DIR + line)
        elif (selected == '6'):
            sparrow(INSTANCES_DIR + line)

        line = instance_file.readline().rstrip()

else:

    config = args.config
    instance_file = open(args.file, 'r')
    line = instance_file.readline().rstrip()
    solved = 0

    while line != '':

        if (config[solved] == '1'):
            ccanr_glucose(INSTANCES_DIR + line)
        elif (config[solved] == '2'):
            glueSplit(INSTANCES_DIR + line)
        elif (config[solved] == '3'):
            lingeling(INSTANCES_DIR + line)
        elif (config[solved] == '4'):
            lingeling_druplig(INSTANCES_DIR + line)
        elif (config[solved] == '5'):
            riss(INSTANCES_DIR + line)
        elif (config[solved] == '6'):
            sparrow(INSTANCES_DIR + line)
        else:
            print 'ERROR: INVALID SOLVER ID!'
            break
        solved += 1
        line = instance_file.readline().rstrip()

