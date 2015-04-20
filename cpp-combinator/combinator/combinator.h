#ifndef __COMBINATOR_H_INCLUDED__
#define __COMBINATOR_H_INCLUDED__

#include <string.h>
#include <stdio.h>
#include "../lib/solver.h"

class Solver;
class InstanceBenchmark;

class Combinator{
    Solver* solvers;
    std::string* instances;
    int combination_length;
    int solvers_length;
    bool debug_lv1;
    bool debug_lv2;

    Solver* build_solver_list();
    std::string* build_instance_list();

    public:
        double solve(int*);
        double solve(int, std::string);
        double solve(int);
        int get_combination_length();
        Solver* get_solvers();
        std::string get_instaces();
        Combinator(std::string**, std::string, std::string,
                   bool, bool, int);
};

#endif
