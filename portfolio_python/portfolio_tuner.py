#! /usr/bin/env python2.7
#
# Autotune a portfolio configuration.
#
import adddeps
import opentuner
import argparse
from opentuner import ConfigurationManipulator, EnumParameter, MeasurementInterface, Result

class PortfolioTuner(MeasurementInterface):
    def manipulator(self):
        manipulator = ConfigurationManipulator()
        values = [0, 1, 2, 5, 8, 10]
        name = 'solver_'
        for i in range (9):
            manipulator.add_parameter(EnumParameter(name + str(i), values))
        return manipulator

    def run(self, desired_result, input, limit):
        cfg = desired_result.configuration.data
        cmd = CMD
        name = 'solver_'
        for i in range(9):
            cmd += ' ' + str(cfg[name + str(i)])

        run_result = self.call_program(cmd)
        return Result(time=run_result['time'])

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
