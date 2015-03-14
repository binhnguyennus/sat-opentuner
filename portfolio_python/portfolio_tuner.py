#! /usr/bin/env python2.7
#
# Autotune a portfolio configuration.
#
import adddeps
import opentuner
import argparse
from opentuner import ConfigurationManipulator, EnumParameter, MeasurementInterface, Result

class PortfolioManipulator(ConfigurationManipulator):
    def __init__(self):
        super(PortfolioManipulator, self).__init__()

    def validate(self, config):
        values = config.data.values()
        return not (sum(values) > 10 or all([v == 0 for v in values]))

class PortfolioTuner(MeasurementInterface):
    def manipulator(self):
        self.manipulator = PortfolioManipulator()
        values = [0, 1, 2, 5, 8, 10]
        name = 'solver_'
        for i in range (9):
            self.manipulator.add_parameter(EnumParameter(name+str(i), values))
        return self.manipulator

    def run(self, desired_result, input, limit):
        cfg = desired_result.configuration.data
        cmd = CMD
        name = 'solver_'

        for i in range(9):
            cmd += ' ' + str(cfg[name + str(i)])

        if (self.manipulator.validate(desired_result.configuration)):
            run_result = self.call_program(cmd)
            result = run_result['time']
        else:
            result = 99999999 

        return Result(time = result)

    def save_final_config(self, configuration):
        cfg = configuration.data
        cmd = CMD
        name = 'solver_'

        for i in range(9):
            cmd += ' ' + str(cfg[name + str(i)])

        print 'Optimal config written to optimal.txt: ', cmd
        with open('optimal.txt', 'a+') as myfile:
            myfile.write("/usr/bin/time -p " + cmd + "\n")

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(parents=opentuner.argparsers())
    args = argparser.parse_args()

    CMD = 'python sat_solver.py -rs'

    PortfolioTuner.main(args)
