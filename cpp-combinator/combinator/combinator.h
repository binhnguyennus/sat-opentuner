#ifndef __COMBINATOR_H_INCLUDED__
#define __COMBINATOR_H_INCLUDED__

#include <string.h>
#include <stdio.h>
#include <fstream>
#include "../lib/solver.h"

class Solver;
class InstanceBenchmark;

class Combinator{
    Solver* solvers;
    std::string* instances;
    int combination_length;
    int solvers_length;
    bool debug_lvl1;
    bool debug_lvl2;

    void build_solver_list(std::string**);
    void build_instance_list(std::string, std::string);

    public:
        double solve(int*);
        double solve(int, std::string);
        double solve(int);
        int get_combination_length();
        Solver* get_solvers();
        std::string get_instaces();
        Combinator(std::string**, std::string, std::string,
                   bool, bool, int, int);
};

#endif
