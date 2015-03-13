import os
import time
import argparse
from subprocess import call
from multiprocessing import Pool, Value, cpu_count

EXEC_DIR = 'sat-opentuner'
SOLVERS_DIR = 'solvers/'
INSTANCES_DIR = 'instances/sat_lib/'
INSTANCES = 'instance_set_3.txt'

WORKERS = []
POOLS = []

parser = argparse.ArgumentParser()
parser.add_argument('--benchmark',
    dest = 'benchmark_solver', metavar = 's',
    default = '0',
    help = 'The solver to benchmark.')
parser.add_argument('--threads',
    dest = 'threads', metavar = 't',
    default = cpu_count(),
    help = 'The size of the thread Pool.')
parser.add_argument('--debug',
    action = 'store_true',
    default = False,
    help = 'Print commands and solver output.')

def ccanr_glucose(filename):

    cmd = SOLVERS_DIR + 'CCAnrglucose/CCAnr+glucose.sh '
    instance = filename
    args = ' 1 1000'
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

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
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def riss(filename):

    cmd = SOLVERS_DIR + 'Riss/blackbox.sh '
    instance = filename
    args = ' .'
    if DEBUG:
        print cmd + instance + args
        call(cmd + instance + args, shell=True)
    else:
        call(cmd + instance + args, stderr=open(os.devnull, 'wb'), 
            stdout=open(os.devnull, 'wb'), shell=True)
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

solvers = {
    '1': ccanr_glucose,
    '2': glueSplit,
    '3': lingeling,
    '4': lingeling_druplig,
    '5': riss,
    '6': sparrow,
}

def run_benchmark(solver, threads, lines):

        pool = Pool(threads)
        for line in lines:
            pool.apply_async(solvers[solver], 
                    args=(INSTANCES_DIR + line, ))

        pool.close()
        pool.join()

def terminate_all_pools(result):

    for pool in POOLS:
        pool.terminate()
        
if __name__ == '__main__':

    PROJECT_DIR = os.getcwd().split(EXEC_DIR)[0]
    os.chdir(PROJECT_DIR + EXEC_DIR)
    args = parser.parse_args()

    benchmark_solver = args.benchmark_solver
    threads = int(args.threads)

    with open(INSTANCES, 'r') as instance_file:    
        lines = instance_file.read().splitlines()

    if (int(benchmark_solver) > 0):
        run_benchmark (benchmark_solver, threads, lines)

    else:
        POOLS.append(Pool(cpu_count()))
        POOLS.append(Pool(cpu_count()))

        WORKERS.append(POOLS[0].map_async(solvers['1'],
            iterable=[INSTANCES_DIR + l for l in lines],
            callback=terminate_all_pools))

        WORKERS.append(POOLS[1].map_async(solvers['2'],
            iterable=[INSTANCES_DIR + l for l in lines],
            callback=terminate_all_pools))

        for pool in POOLS:
            pool.close()

