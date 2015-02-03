#!/usr/bin/env python2.7
#
# Autotune a composition of SAT solvers.
#
import adddeps

import opentuner
from opentuner import ConfigurationManipulator
from opentuner import EnumParameter 
from opentuner import IntegerParameter
from opentuner import MeasurementInterface
from opentuner import Result

SOLVERS = ('i', 1, 6)
INSTANCE_FILE = ' --instance-file instance_set_3.txt'
BENCHMARK = ' --benchmark instances/sat_lib/'
CONFIG = ' --solver-config'
CMD = 'python2 sat_combinator.py'
INSTANCES = 320 
TIMEOUT = 9

class SATTuner(MeasurementInterface):

    def manipulator(self):
        """
        Defining the Search Space.
        """
        manipulator = ConfigurationManipulator()
        param, l_min, l_max = SOLVERS
        for i in range (INSTANCES):
            manipulator.add_parameter(
                    IntegerParameter(param+str(i), l_min, l_max))
        return manipulator

    def run(self, desired_result, input, limit):
        """
        Execute configuration,
        return performance.
        """
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
        """called at the end of tuning"""
        cfg = configuration.data

        param, l_min, l_max = SOLVERS
        cmd = CMD
        cmd += INSTANCE_FILE + BENCHMARK + CONFIG

        for i in range (INSTANCES):

            cmd += ' ' + str(cfg[param + str(i)])

        print "Optimal config written to logs/tuned/tuned_log: ", cmd
        with open("logs/tuned/tuned_log") as f:
            lines = 0
            for lines, l in enumerate(f):
                pass
            lines += 1

        # CHANGE TO WORK WITH BASH
        with open("logs/tuned/tuned_log", "a") as myfile:
            myfile.write("/usr/bin/time -p " + cmd + 
                " &> logs/tuned/tuned{0}.txt".format(lines) + "\n")

if __name__ == '__main__':
    argparser = opentuner.default_argparser()
    SATTuner.main(argparser.parse_args())
