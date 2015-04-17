#ifndef __SOLVER_H_INCLUDED__
#define __SOLVER_H_INCLUDED__

#include <iostream>
#include <string>
#include <stdio.h>
#include <sys/time.h>
#include "InstanceBenchmark.h"

class InstanceBenchmark;

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
               std::string, bool, std::string);
};
#endif
