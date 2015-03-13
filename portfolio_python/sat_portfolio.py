#! /usr/bin/python2
import os
import time
import argparse
import threading
from subprocess import call
from multiprocessing import cpu_count

EXEC_DIR = 'sat-opentuner'
SOLVERS_DIR = 'solvers/'
INSTANCES_DIR = 'instances/sat_lib/'
INSTANCES = 'instance_set_4.txt'

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

class StoppableThread(threading.Thread):

    def __init__(self,target,args):
        super(StoppableThread, self).__init__()
        self._target = target
        self._args = args
        self._stop = threading.Event()

    def stop(self):
        print 'stopped\n'
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        for instance in self._args:
            if self.stopped():
                break
            else:
                self._target(instance)

def ccanr_glucose(instance):

    cmd = SOLVERS_DIR + 'CCAnrglucose/CCAnr+glucose.sh '
    args = ' 1 1000'
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def glueSplit(instance):

    cmd = SOLVERS_DIR + 'glueSplit/glueSplit_clasp '
    args = ''
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def lingeling(instance):

    cmd = SOLVERS_DIR + 'Lingeling/lingeling -v '
    instance = filename
    args = ''
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def lingeling_druplig(instance):

    cmd = SOLVERS_DIR + 'Lingeling/lingeling -v --druplig '
    args = ''
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def riss(instance):

    cmd = SOLVERS_DIR + 'Riss/blackbox.sh '
    args = ' .'
    call(cmd + instance + args, stderr=open(os.devnull, 'wb'), 
        stdout=open(os.devnull, 'wb'), shell=True)
    return

def sparrow(instance):

    cmd = SOLVERS_DIR + 'Sparrow/SparrowToRiss.sh '
    args = ' 1 .'
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

if __name__ == '__main__':

    PROJECT_DIR = os.getcwd().split(EXEC_DIR)[0]
    os.chdir(PROJECT_DIR + EXEC_DIR)
    args = parser.parse_args()

    benchmark_solver = args.benchmark_solver
    threads = int(args.threads)

    with open(INSTANCES, 'r') as instance_file:    
        lines = instance_file.read().splitlines()

    lines = [INSTANCES_DIR + line for line in lines]

    if (int(benchmark_solver) > 0):
        pass

    else:

        test = StoppableThread(target = lingeling_druplig, args = lines)
        test2 = StoppableThread(target = sparrow, args = lines)
        test.start()
        test2.start()
        while True:
            if not test.is_alive():
                test2.stop()
                break
            elif not test2.is_alive():
                test.stop()
                break
            time.sleep(0.01)
