#ifndef __COMBINATOR_H_INCLUDED__
#define __COMBINATOR_H_INCLUDED__

#include <string.h>
#include <stdio.h>
#include <fstream>
#include <getopt.h>
#include "../lib/solver.h"

class Solver;
class InstanceBenchmark;

class Combinator{
    Solver* solvers;
    std::string* instances;
    
    std::string instances_dir;
    std::string instance_file;

    bool debug_lvl1   = false;
    bool debug_lvl2   = false;

    int combination_length;
    int solvers_length;
    int instance_set_size;

    std::string file;

    void build_solver_list(std::string**);
    void build_instance_list(std::string, std::string);
    void load_arguments(int, char**);
    void parse_options();
    void print_configuration();

    public:
        double solve(int*);
        double solve(int, int);
        double solve(int);
        Solver* get_solvers();
        std::string* get_instances();
        Combinator(std::string**, int, int, char**);
};

#endif
