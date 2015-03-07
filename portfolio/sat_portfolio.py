import os
import time
import argparse
from subprocess import call
from multiprocessing import Pool, Value, cpu_count

EXEC_DIR = 'sat-opentuner'
SOLVERS_DIR = 'solvers/'
INSTANCES_DIR = 'instances/sat_lib/'
INSTANCES = 'instance_set_3.txt'

parser = argparse.ArgumentParser()
parser.add_argument('--benchmark',
    dest = 'benchmark_solver', metavar = 's',
    help = 'The solver to benchmark.')
parser.add_argument('--threads',
    dest = 'threads', metavar = 't',
    help = 'The size of the thread Pool.')
parser.set_defaults(benchmark_solver='0')
parser.set_defaults(threads=cpu_count())

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

if __name__ == '__main__':

    PROJECT_DIR = os.getcwd().split(EXEC_DIR)[0]
    os.chdir(PROJECT_DIR + EXEC_DIR)
    args = parser.parse_args()

    benchmark_solver = args.benchmark_solver
    threads = int(args.threads)

    solvers = {
        '1': ccanr_glucose,
        '2': glueSplit,
        '3': lingeling,
        '4': lingeling_druplig,
        '5': riss,
        '6': sparrow,
    }

    with open(INSTANCES, 'r') as instance_file:    
        lines = instance_file.read().splitlines()

    if (int(benchmark_solver) > 0):

        pool = Pool(threads)
        for line in lines:
            pool.apply_async(solvers[benchmark_solver], 
                    args=(INSTANCES_DIR + line, ))

        pool.close()
        pool.join()
    else:
        workers = []
        pools = []

        pools.append(Pool(cpu_count()))
        pools.append(Pool(cpu_count()))

        workers.append(pools[0].map_async(solvers['1'],
            iterable=[INSTANCES_DIR + l for l in lines]))

        workers.append(pools[1].map_async(solvers['4'],
            iterable=[INSTANCES_DIR + l for l in lines]))

        for pool in pools:
            pool.close()
        
        while True:
            if any(worker.ready() for worker in workers):
                print [w.ready() for w in workers]
                for pool in pools:
                    pool.terminate()

                break
