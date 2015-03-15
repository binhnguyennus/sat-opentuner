#! /usr/bin/env python2.7
#
# Autotune a portfolio configuration.
#
import adddeps
import opentuner
import argparse
from opentuner import ConfigurationManipulator, EnumParameter
from opentuner import MeasurementInterface, Result, ParameterArray

class PortfolioManipulator(ConfigurationManipulator):
    def __init__(self, max_sum):
        self._max_sum = max_sum 
        super(PortfolioManipulator, self).__init__()

    def validate(self, config):
        values = config.values()
        return not (sum(values) > self._max_sum or 
                    all([v == 0 for v in values]))

    def random(self):
        cfg = self.seed_config()
        while (not self.validate(cfg)):
            for p in self.parameters(cfg):
                p.op1_randomize(cfg)
        return cfg

class PortfolioTuner(MeasurementInterface):
    def manipulator(self):
        self._manipulator = PortfolioManipulator(self._max_sum)
        for i in range (self._solvers):
            self._manipulator.add_parameter(EnumParameter(self._names + str(i),
                                                          self._values))
        return self._manipulator

    def run(self, desired_result, input, limit):
        cfg = desired_result.configuration.data
        if (self._manipulator.validate(cfg)):
            cmd = self._cmd
            for i in range(self._solvers):
                cmd += ' ' + str(cfg[self._names + str(i)])
            result = self.call_program(cmd, limit = self._timeout)['time']
        else:
            result = self._timeout
        return Result(time = result)

    def save_final_config(self, configuration):
        cfg = configuration.data
        cmd = self._cmd

        for i in range(self._solvers):
            cmd += ' ' + str(cfg[self._names + str(i)])

        print 'Optimal config written to optimal.txt: ', cmd
        with open('optimal.txt', 'a+') as myfile:
            myfile.write("/usr/bin/time -p " + cmd + "\n")

    @classmethod
    def init(self, max_sum, solvers, values, timeout, cmd):
        self._max_sum = max_sum
        self._solvers = solvers
        self._values = values
        self._timeout = timeout
        self._names = 'solver_'
        self._cmd = cmd

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(parents=opentuner.argparsers())
    _args = argparser.parse_args()

    PortfolioTuner.init(max_sum = 8,
                        solvers = 9,
                        values = [0, 1, 2, 5],
                        timeout = 120,
                        cmd = 'python sat_solver.py -rs')
    PortfolioTuner.main(_args)
