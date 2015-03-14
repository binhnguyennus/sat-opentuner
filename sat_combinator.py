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
parser.add_argument('--debug',
        dest = 'debug',
        action = 'store_true',
        help = 'Print commands and solver output.')
parser.set_defaults(single = False)
parser.set_defaults(solve_all = False)
parser.set_defaults(debug = False)

def glueSplit(filename):

    cmd = SOLVERS_DIR + 'glueSplit/glueSplit_clasp '
    instance = filename
    args = ''
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def lingeling(filename):

    cmd = SOLVERS_DIR + 'Lingeling/lingeling -v '
    instance = filename
    args = ''
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def lingeling_druplig(filename):

    cmd = SOLVERS_DIR + 'Lingeling/lingeling -v --druplig '
    instance = filename
    args = ''
    if (DEBUG):
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def sparrow(filename):

    cmd = SOLVERS_DIR + 'Sparrow/SparrowToRiss.sh '
    instance = filename
    args = ' 1 .'
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stderr=open(os.devnull, 'wb'),
            stdout=open(os.devnull, 'wb'), shell=True)
    return

def minisat_blbd(filename):

    cmd = SOLVERS_DIR + 'minisat_blbd/minisat_blbd '
    instance = filename
    args = ''
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stderr=open(os.devnull, 'wb'), 
            stdout=open(os.devnull, 'wb'), shell=True)
    return

def sgseq(filename):

    cmd = SOLVERS_DIR + 'SGSeq/SGSeq.sh '
    instance = filename
    args = ''
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stderr=open(os.devnull, 'wb'), 
            stdout=open(os.devnull, 'wb'), shell=True)
    return

def glucose(filename):

    cmd = SOLVERS_DIR + 'glucose/glucose '
    instance = filename
    args = ''
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stderr=open(os.devnull, 'wb'), 
            stdout=open(os.devnull, 'wb'), shell=True)
    return

def cryptominisat(filename):

    cmd = SOLVERS_DIR + 'cryptominisat/cryptominisat '
    instance = filename
    args = ''
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stderr=open(os.devnull, 'wb'), 
            stdout=open(os.devnull, 'wb'), shell=True)
    return

solvers = {
    '1' : glueSplit,
    '2' : lingeling,
    '3' : lingeling_druplig,
    '4' : sparrow,
    '5' : minisat_blbd,
    '6' : sgseq,
    '7' : glucose,
    '8' : cryptominisat,
}

def solve_instance(solver, instance_path):

    solvers[solver](instance_path)

if __name__ == '__main__':

    args = parser.parse_args()
    single_solve = args.single
    solve_all = args.solve_all
    INSTANCES_DIR = args.benchmark
    DEBUG = args.debug

    if single_solve:

        target = args.target
        selected = args.selected
        line = linecache.getline(args.file, int(target)).rstrip()
        solve_instance(selected, INSTANCES_DIR + line)
        linecache.clearcache()

    elif solve_all:

        selected = args.selected
        instance_file = open(args.file, 'r')
        line = instance_file.readline().rstrip() 
        while line != '':
            
            solve_instance(selected, INSTANCES_DIR + line)
            line = instance_file.readline().rstrip()

    else:

        config = args.config
        instance_file = open(args.file, 'r')
        line = instance_file.readline().rstrip()
        solved = 0
        while line != '':

            solve_instance(config[solved], INSTANCES_DIR + line)
            solved += 1
            line = instance_file.readline().rstrip()

