#ifndef __SOLVER_H_INCLUDED__
#define __SOLVER_H_INCLUDED__

#include <iostream>
#include <string>
#include "Benchmark.h"

class Benchmark;

class Solver {
    std::string name;
    std::string cmd;
    std::string args;
    bool debug;

    public:
        std::string get_name ();
        float solve(std::string);
        Benchmark benchmark(std::string, int);
        Solver (std::string, std::string, std::string, bool);
};
#endif
