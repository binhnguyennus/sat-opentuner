#!/usr/bin/env python2.7
#
# Autotune a composition of SAT solvers.
#
import adddeps
import argparse
import opentuner
from opentuner import ConfigurationManipulator
from opentuner import EnumParameter 
from opentuner import IntegerParameter
from opentuner import MeasurementInterface
from opentuner import Result

argparser = argparse.ArgumentParser(parents=opentuner.argparsers())
argparser.add_argument('--instance-set',
        dest = 'instances', metavar = 'I',
        help = 'The file containing all possible instances to solve')
argparser.add_argument('--benchmark',
        dest = 'benchmark', metavar = 'B',
        help = 'The directory containing all the instances.')
argparser.add_argument('-i', dest = 'instance_number',
        help = 'Number of instances to solve.')
argparser.add_argument('--timeout', 
        dest = 'timeout', metavar = 't',
        help = 'Time cutoff for solving a single instance.')
argparser.add_argument('--logdir',
        dest = 'log_dir',
        required = True,
        help = 'The directory to write the logs.')
argparser.add_argument('--bestlog',
        dest = 'log_file',
        required = True,
        help = 'File to log the best configurations over several runs.')
argparser.add_argument('--log-best-data',
        dest = 'log_best',
        action = 'store_true',
        help = 'Saves the best configuration as a JSON file.')

argparser.set_defaults(timeout = 20)
argparser.set_defaults(instance_number = 320)
argparser.set_defaults(benchmark = 'instances/sat_lib/')
argparser.set_defaults(instances = 'instance_set_3.txt')
argparser.set_defaults(log_best = False)

class SATTuner(MeasurementInterface):
    def manipulator(self):
        manipulator = ConfigurationManipulator()
        param, l_min, l_max = SOLVERS
        for i in range (INSTANCES):
            manipulator.add_parameter(
                    IntegerParameter(param+str(i), l_min, l_max))
        return manipulator

    def run(self, desired_result, input, limit):
        cfg = desired_result.configuration.data

        param, l_min, l_max = SOLVERS

        cmd = CMD
        cmd += INSTANCE_FILE + BENCHMARK + CONFIG
        for i in range (INSTANCES):
            cmd += ' ' + str(cfg[param + str(i)])

        run_result = self.call_program(cmd, limit=TIMEOUT)
        if (run_result['timeout']):
            result = TIMEOUT
        else:
            result = run_result['time']
        return Result(time=result)

    def save_final_config(self, configuration):
        cfg = configuration.data

        param, l_min, l_max = SOLVERS
        cmd = CMD
        cmd += INSTANCE_FILE + BENCHMARK + CONFIG
        if (LOG_BEST):
            print "Optimal configuration written to 'final_config.json'."
            self.manipulator().save_to_file(cfg, LOG_DIR + 'final_config.json')

        for i in range (INSTANCES):
            cmd += ' ' + str(cfg[param + str(i)])

        print "Optimal config written to " + LOG_DIR + LOG_FILE + ": ", cmd
        with open(LOG_DIR + LOG_FILE, 'a+') as myfile:
            myfile.write("/usr/bin/time -p " + cmd + "\n")

if __name__ == '__main__':
    args = argparser.parse_args()

    SOLVERS = ('i', 1, 4)
    INSTANCE_FILE = ' --instance-file ' + args.instances
    LOG_DIR = args.log_dir
    LOG_FILE = args.log_file
    LOG_BEST = args.log_best
    BENCHMARK = ' -id ' + args.benchmark
    CONFIG = ' --solver-config'
    CMD = 'python sat_combinator.py'
    INSTANCES = int(args.instance_number)
    TIMEOUT = int(args.timeout)

    SATTuner.main(args)
