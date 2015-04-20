#ifndef __SOLVER_H_INCLUDED__
#define __SOLVER_H_INCLUDED__

#include <iostream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

class InstanceBenchmark {
    std::string instance;
    std::string solver;
    double median, mean, stddev;
    double* values;

    double calc_median();
    double calc_mean();
    double calc_stddev();

    public:
        double* get_values();
        double get_median();
        double get_mean();
        double get_stddev();

        std::string get_solver_name();
        std::string get_instance_name();
        InstanceBenchmark(std::string, std::string, double*);
};

class Solver {
    std::string name;
    std::string cmd;
    std::string args;
    std::string separator;
    int id;
    bool debug;

    public:
        std::string get_name();
        int get_id();
        double solve(std::string);
        InstanceBenchmark benchmark(std::string, int);
        Solver(int, std::string, std::string, 
               std::string, bool);
};
#endif
