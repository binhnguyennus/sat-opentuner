#include "../lib/solver.h"
#include "combinator.h"
#include <stdio.h>

Combinator::Combinator(std::string** solver_values,
                       std::string instances_dir,
                       std::string instance_file,
                       bool new_debug_lvl1,
                       bool new_debug_lvl2,
                       int new_solvers_length,
                       int new_combination_length){
    solvers_length     = new_solvers_length;
    combination_length = new_combination_length;
    debug_lvl1         = new_debug_lvl1;
    debug_lvl2         = new_debug_lvl2;

    Solver solvers [solvers_length];
    std::string instances [combination_length];
    build_solver_list(solver_values);
    build_instance_list(instances_dir, instance_file);
}

void Combinator::build_solver_list(std::string** values){
    for (int i = 0; i < solvers_length; i++){
        solvers[i] = Solver(i, values[i][0], values[i][0],
                                values[i][1], debug_lvl2);
    }
}

void Combinator::build_instance_list(std::string dir,
                                     std::string file){
    std::ifstream infile(file.c_str());
    std::string instance;
    for (int i = 0; i < combination_length; i++){
        infile >> instance;
        instances[i] = dir + instance;
    }
}

int main(){
    Solver s (0, "test_name", "test_cmd",
              "test_args", true);
    printf("name: %s\n", s.get_name().c_str());
    printf("time_to_solve: %f\n", s.solve("test_instance"));
    printf("id: %d\n", s.get_id());
    InstanceBenchmark b = s.benchmark("test_instance", 10);
    printf("instance_name: %s\n", b.get_instance_name().c_str());
    double* results = b.get_values();
    for (int i = 0; i < 10; i++){
        printf("results[%d]=%f\n", i, results[i]);
    }
    return 0;
}
