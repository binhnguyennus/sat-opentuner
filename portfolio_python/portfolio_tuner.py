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
        values = [1, 2, 5, 8, 10]
        name = 'solver_'
        for i in range (9):
            manipulator.add_parameter(EnumParameter(name + str(i), values))
        return manipulator

    def run(self, desired_result, input, limit):
        return Result()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(parents=opentuner.argparsers())
    args = argparser.parse_args()

    PortfolioTuner.main(args)
