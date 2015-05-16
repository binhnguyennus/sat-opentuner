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
from opentuner import IntegerParameterArray
from opentuner import MeasurementInterface
from opentuner import Result

argparser = argparse.ArgumentParser(parents=opentuner.argparsers())
argparser.add_argument('-f', '--instance-set',
        dest = 'instances',
        default = 'instance_set_3.txt',
        help = 'The file containing a subset of instances to solve')
argparser.add_argument('-c', '--chunk-number',
        dest = 'chunks',
        default = 2,
        help = 'The number of subdivisions of the instance set.')
argparser.add_argument('-id', '--instance-directory',
        dest = 'instances_dir',
        default = 'instances/sat_lib/',
        help = 'The directory containing all the instances.')
argparser.add_argument('-i',
        dest = 'instance_number',
        default = 320,
        help = 'Number of instances to solve.')
argparser.add_argument('-to', '--timeout',
        dest = 'timeout',
        default = 20,
        help = 'Time cutoff for solving a single instance.')
argparser.add_argument('-ld', '--logdir',
        dest = 'log_dir',
        required = True,
        help = 'The directory to write the logs.')
argparser.add_argument('-lfb', '--bestlog',
        dest = 'log_file',
        required = True,
        help = 'File to log the best configurations over several runs.')
argparser.add_argument('-lb', '--log-best-data',
        dest = 'log_best',
        action = 'store_true',
        default = False,
        help = 'Saves the best configuration as a JSON file.')

class SATTuner(MeasurementInterface):
    def manipulator(self):
        manipulator = ConfigurationManipulator()
        solvers, s_min, s_max = SOLVERS

        manipulator.add_parameter(
                IntegerParameterArray("instances", [s_min]*CHUNKS,
                                      [s_max]*CHUNKS))

        return manipulator

    def run(self, desired_result, input, limit):
        cfg = desired_result.configuration.data

        solver = SOLVERS[0]
        cmd = CMD
        cmd += INSTANCE_FILE + BENCHMARK + CONFIG
        j = 0

        for i in range (INSTANCES):
            cmd += ' ' + str(cfg["instances"][j])
            if ((i > 0 and j < len(cfg["instances"]) - 1 
                       and i % CHUNK_SIZE == 0) 
                       or (i == 0 and CHUNKS == INSTANCES)):
                j += 1

        run_result = self.call_program(cmd, limit=TIMEOUT)
        if (run_result['timeout']):
            result = TIMEOUT
        else:
            result = run_result['time']

        stdout = run_result['stdout']
        stdout_time = float(stdout.split("Time: ")[1])
        return Result(time=stdout_time)

    def save_final_config(self, configuration):
        cfg = configuration.data

        solver = SOLVERS[0]
        cmd = 'python ../../../combinator.py'
        cmd += INSTANCE_FILE + BENCHMARK + CONFIG
        if (LOG_BEST):
            print "Optimal configuration written to 'final_config.json'."
            self.manipulator().save_to_file(cfg, LOG_DIR + 'final_config.json')

        j = 0

        for i in range (INSTANCES):
            cmd += ' ' + str(cfg["instances"][j])
            if ((i > 0 and j < len(cfg["instances"]) - 1 
                       and i % CHUNK_SIZE == 0)
                       or (i == 0 and CHUNKS == INSTANCES)):
                j += 1

        print "Optimal config written to " + LOG_DIR + LOG_FILE + ": ", cmd
        with open(LOG_DIR + LOG_FILE, 'a+') as myfile:
            myfile.write(cmd + "\n")

if __name__ == '__main__':
    args = argparser.parse_args()

    SOLVERS = ('i', 0, 6)
    CHUNKS = int(args.chunks)
    INSTANCE_FILE = ' -f ' + args.instances
    LOG_DIR = args.log_dir
    LOG_FILE = args.log_file
    LOG_BEST = args.log_best
    BENCHMARK = ' -id ' + args.instances_dir
    CONFIG = ' --solver-config'
    CMD = 'python combinator.py '
    INSTANCES = int(args.instance_number)
    TIMEOUT = int(args.timeout)

    CHUNK_SIZE = int(INSTANCES / CHUNKS)

    SATTuner.main(args)
