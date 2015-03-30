#! /usr/bin/env python2
#
# Brute Force Searcher for a
# set of instances and solvers.
#
# Outputs the best configuration
# to a file.
#
import argparse
import linecache
import os
import time
import math
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

    def calc_stddev(self):
        average = self.average()
        temp = [(v - average) ** 2 for v in self._values]
        return math.sqrt(sum(temp) / len(self._values))

    def median(self):
        return self._median

    def average(self):
        return self._average

    def stddev(self):
        return self._stddev

    def solver(self):
        return self._solver

    def instance(self):
        return self._instance

    def __init__(self, values, solver, instance):
        self._solver = solver
        self._instance = instance
        self._values = values
        self._median = self.calc_median()
        self._average = self.calc_average()
        self._stddev = self.calc_stddev()

class Solver:
    def benchmark(self, instance, runs):
        times = []
        for i in range(runs):
            start = time.time()
            self._solve(instance)
            times.append(time.time() - start)

        return Benchmark(times, self._name, instance)

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
    def log(self):
        times =  open('brute-force/logtimes.txt', 'w+')
        configuration = open('brute-force/logconfig.txt', 'w+')
        for b in self._best:
            times.write(', '.join(map(str,b)) + '\n')
            configuration.write(str(solvers[b[0]]) + ' ')

    def find_best(self):
        print '> Finding best solver for each instance.'
        self._best = []
        for benchmark in self._instance_benchmarks:
            averages = [solver.average() for solver in benchmark]
            min_index = 0
            for i in range(1, len(averages)):
                if (averages[i] < averages[min_index]):
                    min_index = i

            best_b = benchmark[min_index]
            self._best.append([best_b.solver(), best_b.instance(), best_b.average(), best_b.stddev()])

        print '> Done.'
        return self._best

    def benchmark(self):
        print '> Starting Benchmarks.'
        for i in range(len(self._instances)):
            print '> Solving instance: {0}'.format(i)
            if self._debug:
                print '> Starting Benchmark of instance {0} :'.format(self._instances[i])
            self._instance_benchmarks.append([])
            for solver in self._solvers:
                if self._debug:
                    print '>    With solver {0}.'.format(solver.name())
                self._instance_benchmarks[i].append(
                        solver.benchmark(self._instances[i], self._runs))
                if self._debug:
                    print '>    Done.'

        print '> Done.'

    def __init__(self, solver_names, instances_dir, instances, runs, debug1, debug2):
        with open(instances, 'r') as instance_file:
            self._instances = instance_file.read().splitlines()

        print '> Initializing Brute Force Searcher.'
        print '>    Number of runs in each benchmark: {0}'.format(runs)
        self._instances = [instances_dir + i for i in self._instances]
        self._solver_names = solver_names
        self._runs = runs
        self._debug = debug1

        self._best = []
        self._solvers = []
        self._instance_benchmarks = []
        for i in range(len(solver_names)):
            self._solvers.append(Solver(solver_names[i][0], solver_names[i][0],
                                        solver_names[i][1], debug2))

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
parser.add_argument('-v', '--debug1',
    dest = 'debug1',
    action = 'store_true',
    default = False,
    help = 'Print debugging messages for the Brute Force Searcher.')
parser.add_argument('-vv', '--debug2',
    dest = 'debug2',
    action = 'store_true',
    default = False,
    help = 'Print debugging messages for the solvers.')
parser.add_argument('-vvv', '--debug3',
    dest = 'debug3',
    action = 'store_true',
    default = False,
    help = 'Print all debugging messages. (VERY verbose)')

exec_dir = 'sat-opentuner'
project_dir = os.getcwd().split(exec_dir)[0]
os.chdir(project_dir + exec_dir)

args = parser.parse_args()
solvers_dir = args.solvers_dir
instances_dir = args.instances_dir
instances = args.instances
runs = int(args.runs)
debug1 = args.debug1
debug2 = args.debug2
debug3 = args.debug3

if debug3:
    debug1 = debug3
    debug2 = debug3

if __name__ == '__main__':

    solver_ids = [(solvers_dir + 'glueSplit/glueSplit_clasp ', ''),
                  (solvers_dir + 'Lingeling/lingeling -v ', ''),
                  (solvers_dir + 'Lingeling/lingeling -v --druplig ', ''),
                  (solvers_dir + 'Sparrow/SparrowToRiss.sh ', ' 1 .'),
                  (solvers_dir + 'minisat_blbd/minisat_blbd ', ''),
                  (solvers_dir + 'SGSeq/SGSeq.sh ', ''),
#                 (solvers_dir + 'glucose/glucose ', ''),
                  (solvers_dir + 'cryptominisat/cryptominisat ', ''),
                  (solvers_dir + 'CCAnrglucose/CCAnr+glucose.sh ', ' 1 1000')]

    solvers = {
        solvers_dir + 'glueSplit/glueSplit_clasp '        : 1,
        solvers_dir + 'Lingeling/lingeling -v '           : 2,
        solvers_dir + 'Lingeling/lingeling -v --druplig ' : 3,
        solvers_dir + 'Sparrow/SparrowToRiss.sh '         : 4,
        solvers_dir + 'minisat_blbd/minisat_blbd '        : 5,
        solvers_dir + 'SGSeq/SGSeq.sh '                   : 6,
        solvers_dir + 'cryptominisat/cryptominisat '      : 7,
        solvers_dir + 'CCAnrglucose/CCAnr+glucose.sh '    : 8,
#       solvers_dir + 'glucose/glucose '                  : 9,
        }


    searcher = Searcher(solver_ids, instances_dir, instances, runs, debug1, debug2)
    searcher.benchmark()
    best = searcher.find_best()
    searcher.log()
