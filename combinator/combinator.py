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

class Solver:
    def solve(self, instance):
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

class Combinator:
    def _combination(self, combination):
        if self._debug:
            print '> Starting to solve a combination.'
        for i in range(len(combination)):
            self._single(int(combination[i]), i)

    def _all(self, solver):
        if self._debug:
            print '> Starting to solve all instances with {0}.'.format(self._solvers[solver].name())
        combination = [solver]*len(self._instances)
        self._combination(combination)

    def _single(self, solver, target_instance):
        if self._debug:
            print '> Solving {0} with {1}.'.format(self._instances[target_instance], self._solvers[solver].name())
        self._solvers[solver].solve(self._instances[target_instance])

    def solve(self, combination = None, solver = None, target_instance = None):
        if combination:
            self._combination(combination)
        elif self._solve_all:
            self._all(solver)
        elif target_instance != None:
            self._single(solver, target_instance)

    def __init__(self, solver_names, instances,
                 instances_dir, single_solve,
                 solve_all, debug1, debug2):
        with open(instances, 'r') as instance_file:
            self._instances = instance_file.read().splitlines()

        self._instances = [instances_dir + i for i in self._instances]
        self._solver_names = solver_names
        self._debug = debug1
        self._solve_all = solve_all
        self._single_solve = single_solve

        self._solvers = []
        for i in range(len(solver_names)):
            self._solvers.append(Solver(solver_names[i][0], solver_names[i][0],
                                        solver_names[i][1], debug2))

start = time.time()
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--solver-config', nargs = '+',
    dest = 'config',
    default = None,
    help = 'A sequence of integers specifying a solver sequence.')
parser.add_argument('-f', '--instance-file',
    dest = 'instances',
    default = 'sets/instance_set_6.txt',
    help = 'A file containing a subset of instances to solve.')
parser.add_argument('-sg', '--single-solve',
    dest = 'single',
    action = 'store_true',
    default = False,
    help = 'Solves a single instance with a given solver.')
parser.add_argument('-t', '--target-instance',
    dest = 'target',
    default = None,
    help = 'The instance to solve. (only when --single-solve is passed)')
parser.add_argument('-ss', '--select-solver',
    dest = 'selected',
    default = None,
    help = 'The solver to be used. (only when --single-solver is passed)')
parser.add_argument('-id', '--instance-directory',
    dest = 'instances_dir',
    default = 'instances/sat_lib_harder/',
    help = 'The directory with all instances to solve.')
parser.add_argument('-sa', '--solve-all',
    dest = 'solve_all',
    action = 'store_true',
    default = False,
    help = 'Solves all instances with a given solver.')
parser.add_argument('-s', '--solvers-directory',
    dest = 'solvers_dir',
    default = 'solvers/',
    help = 'The directory containing the solver binaries.')
parser.add_argument('-v', '--debug1',
    dest = 'debug1',
    action = 'store_true',
    default = False,
    help = 'Print debugging messages for the Combinator.')
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
instances = args.instances
instances_dir = args.instances_dir
target_instance = int(args.target) if args.target else args.target
config = args.config
single_solve = args.single
solve_all = args.solve_all
selected = int(args.selected) if args.selected else args.selected
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
        (solvers_dir + 'cryptominisat/cryptominisat ', '')]
#        (solvers_dir + 'CCAnrglucose/CCAnr+glucose.sh ', ' 1 1000')]

    solvers = {
        solvers_dir + 'glueSplit/glueSplit_clasp '        : 0,
        solvers_dir + 'Lingeling/lingeling -v '           : 1,
        solvers_dir + 'Lingeling/lingeling -v --druplig ' : 2,
        solvers_dir + 'Sparrow/SparrowToRiss.sh '         : 3,
        solvers_dir + 'minisat_blbd/minisat_blbd '        : 4,
        solvers_dir + 'SGSeq/SGSeq.sh '                   : 5,
        solvers_dir + 'cryptominisat/cryptominisat '      : 6,
#        solvers_dir + 'CCAnrglucose/CCAnr+glucose.sh '    : 7,
        }

    combinator = Combinator(solver_ids, instances,
                            instances_dir, single_solve,
                            solve_all, debug1, debug2)

    if (selected != None and target_instance != None):
        combinator.solve(solver = selected, target_instance = target_instance)
    elif config:
        combinator.solve(combination = config)
    elif (selected != None and solve_all):
        combinator.solve(solver = selected)

    print '> Time: {}'.format(time.time() - start)
