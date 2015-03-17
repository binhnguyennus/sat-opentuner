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
import time
from subprocess import call

class Benchmark:
    def values(self):
        return self._values

    def calc_median(self):
        _values = sorted(self._values)
        size = len(_values)
        if (size < 1):
                return None
        if (size % 2 == 1):
                return _values[((size + 1) / 2) - 1]
        if (size % 2 == 0):
                return float(sum(_values[(size / 2) - 1:(size / 2) + 1])) / 2.0

    def calc_average(self):
        return sum(self._values) / len(self._values)

    def median(self):
        return self._median

    def average(self):
        return self._average

    def solver(self):
        return self._solver

    def instance(self):
        return self.instance

    def __init__(self, values, solver, instance):
        self._solver = solver
        self._instance = instance
        self._values = values
        self._median = self.calc_median()
        self._average = self.calc_average()

class Solver:
    def benchmark(self, instance, runs):
        times = []
        for i in range(runs):
            start = time.time()
            self._solve(instance)
            times.append(time.time() - start)

        return Benchmark(times, self.name, instance)

    def _solve(self, instance):
        cmd = self._cmd + instance + self._args
        if self._debug:
            print cmd
            call(cmd, shell = True)
        else:
            call(cmd, stderr = open(os.devnull, 'wb'),
                 stdout = open(os.devnull, 'wb'), shell = True)

    def name(self):
        return self._name

    def __init__(self, name, cmd, args, debug):
        self._name = name
        self._cmd = cmd
        self._args = args
        self._debug = debug

class Searcher:
    def benchmark():
        for i in range(len(self._instances)):
            if self_debug:
                print '> Starting Benchmark of instance ' + self._instances[i] + ':'
            self._instance_benchmarks.append([])
            for solver in self._solvers:
                if self._debug:
                    print '>    With solver ' + solver.name() + '.' 
                self._instance_benchmarks[i].append(
                        solver.benchmark(self._instances[i], self._runs))
                if self._debug:
                    print '>    Done.'

    def __init__(self, solver_names, instances_dir, instances, runs, debug):
        with open(instances, 'r') as instance_file:
            self._instances = instance_file.read().splitlines()

        self._instances = [instances_dir + i for i in self._instances]
        self._solver_names = solver_names
        self._runs = runs
        self._debug = debug

        self._solvers = []
        self._instance_benchmarks = []
        for i in range(len(solver_names)):
            self._solvers.append(Solver(solver_names[i][0], solver_names[i][0],
                                        solver_names[i][1], debug))

parser = argparse.ArgumentParser()
parser.add_argument('-id', '--instance-directory', 
    dest = 'instances_dir',
    default = 'instances/sat_lib/',
    help = 'The directory containing instances to be solved.')
parser.add_argument('-f', '--instance-file',
    dest = 'instances',
    default = 'sets/instance_set_3.txt',
    help = 'The file with the names of the selected instances.')
parser.add_argument('-s', '--solvers-directory',
    dest = 'solvers_dir',
    default = 'solvers/',
    help = 'The directory containing the solver binaries.')
parser.add_argument('-r', '--runs',
    dest = 'runs',
    default = '20',
    help = 'The number of runs in the benchmarks.')
parser.add_argument('-d', '--debug',
    dest = 'debug',
    action = 'store_true',
    default = False,
    help = 'Print debugging messages.')

exec_dir = 'sat-opentuner'
project_dir = os.getcwd().split(exec_dir)[0]
os.chdir(project_dir + exec_dir)

if __name__ == '__main__':

    args = parser.parse_args()
    solvers_dir = args.solvers_dir
    instances_dir = args.instances_dir
    instances = args.instances
    runs = args.runs
    debug = args.debug

    solver_ids = [(solvers_dir + 'glueSplit/glueSplit_clasp ', ''),
                  (solvers_dir + 'Lingeling/lingeling -v ', ''),
                  (solvers_dir + 'Lingeling/lingeling -v --druplig ', ''),
                  (solvers_dir + 'Sparrow/SparrowToRiss.sh ', ' 1 .'),
                  (solvers_dir + 'minisat_blbd/minisat_blbd ', ''),
                  (solvers_dir + 'SGSeq/SGSeq.sh ', ''),
                  (solvers_dir + 'glucose/glucose ', ''),
                  (solvers_dir + 'cryptominisat/cryptominisat ', ''),
                  (solvers_dir + 'CCAnrglucose/CCAnr+glucose.sh ', ' 1 1000')]

    searcher = Searcher(solver_ids, instances_dir, instances, runs, debug)
