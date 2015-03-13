#! /usr/bin/python2
import os
import time
import argparse
import threading
from subprocess import call
from multiprocessing import cpu_count

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

    def __init__(self, target, args):

        super(StoppableThread, self).__init__()
        self._target = target
        self._args = args
        self._stop = threading.Event()

    def stop(self):

        self._stop.set()

    def stopped(self):

        return self._stop.isSet()

    def run(self):

        for instance in self._args:
            if self.stopped():
                break
            else:
                self._target(instance)

class Solver:

    def solve(self, instance):
        cmd = self.cmd + instance + self.cmd_args
        if self.debug:
            print cmd
            call(cmd, shell=True)
        else:
            call(cmd, stderr=open(os.devnull, 'wb'), 
                stdout=open(os.devnull, 'wb'), shell=True)
        return

    def create_threads(self):

        for instance in self.instances:
            self.threads.append(StoppableThread(target = self.solve, 
                args = instance))

        print self.threads
        return

    def start(self):
        
        for thread in self.threads:
            thread.start()
        return

    def is_alive(self):

        return any([thread.is_alive() for thread in self.threads])

    def stop(self):

        for thread in self.threads:
            thread.stop()
        return

    def __init__(self, cmd, cmd_args, instances, debug):

        self.cmd = cmd
        self.cmd_args = cmd_args
        self.instances = instances
        self.threads = []
        self.debug = debug

class Portfolio:

    def stop(self):

        for solver in self.solvers:
            solver.stop()
        return

    def solve(self):
        
        for solver in self.solvers:
            solver.create_threads()
            solver.start()

        solving = True
        while solving:
            time.sleep(0.01)
            if any([(not solver.is_alive()) for solver in self.solvers]):
                solving = False

        self.stop()
        return

    def __init__(self, solver_names, instances_dir, instances, 
            resource_sharing, debug):

        with open(instances, 'r') as instance_file:
            self.instances = instance_file.read().splitlines()

        self.instances = [instances_dir + i for i in self.instances]
        self.solver_names = solver_names
        self.resource_sharing = resource_sharing
        self.solvers = []
        self.debug = debug

        for i in range(len(self.resource_sharing)):
            if (resource_sharing[i] > 0):
                self.solvers.append(Solver(solver_names[i][0],
                    solver_names[i][1],
                    zip(*[iter(self.instances)] * (len(self.instances) / resource_sharing[i])),
                    self.debug))
        print self.solvers

if __name__ == '__main__':

    exec_dir = 'sat-opentuner'
    solvers_dir = 'solvers/'
    instances_dir = 'instances/sat_lib/'
    instances = 'instance_set_4.txt'

    project_dir = os.getcwd().split(exec_dir)[0]
    os.chdir(project_dir + exec_dir)
    args = parser.parse_args()

    debug = args.debug

    solvers = [(solvers_dir + 'CCAnrglucose/CCAnr+glucose.sh ', ' 1 1000'),
            (solvers_dir + 'glueSplit/glueSplit_clasp ', ''),
            (solvers_dir + 'Lingeling/lingeling -v ', ''),
            (solvers_dir + 'Lingeling/lingeling -v --druplig ', ''),
            (solvers_dir + 'Riss/blackbox.sh ', ' .'),
            (solvers_dir + 'Sparrow/SparrowToRiss.sh ', ' 1 .')]
    resource_sharing = [0, 0, 0, 10, 0, 0]

    portfolio = Portfolio(solvers,
            instances_dir,
            instances,
            resource_sharing,
            debug)
    portfolio.solve()
