#include "../lib/solver.h"
#include "combinator.h"
#include <stdio.h>

Solver* Combinator::get_solvers(){
    return solvers;
}
std::string* Combinator::get_instances(){
    return instances;
}
void Combinator::build_solver_list(std::string** values){
    for (int i = 0; i < solvers_length; i++){
        if (debug_lvl1){
            printf("Creating Solver \"%s\" with Args \"%s\" and ID %d.\n",
                   values[i][0].c_str(), values[i][1].c_str(), i);
        }
        solvers[i] = Solver(i, values[i][0], values[i][0],
                            values[i][1], debug_lvl2);
    }
}
void Combinator::build_instance_list(std::string dir,
                                     std::string file){
    std::ifstream infile(file.c_str());
    std::string instance;
    if (!infile.fail()){
        for (int i = 0; i < combination_length; i++){
            infile >> instance;
            instances[i] = dir + instance;
            if (debug_lvl1){
                printf("Instance Added: \"%s\"\n", instances[i].c_str());
            }
        }
    }
    else if (debug_lvl1){
        printf("Error opening file: \"%s\"\n", file.c_str());
    }
}
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

    solvers = new Solver[solvers_length];
    instances = new std::string[combination_length];
    if (debug_lvl1){
        printf("\nCreating Combinator: \n");
        printf("Solvers: %d\n", solvers_length);
        printf("Combination Length: %d\n", combination_length);
        printf("Debug_LVL2: %d\n", debug_lvl2);
        printf("Instance File: %s\n", instance_file.c_str());
        printf("Instances Dir: %s\n", instances_dir.c_str());
        printf("\nInitializing Solver List:\n");
    }
    build_solver_list(solver_values);
    if (debug_lvl1){
        printf("Initializing Instance List.\n");
    }
    build_instance_list(instances_dir, instance_file);
}
void test_solver(){
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
}
void test_combinator(){
    std::string** p = new std::string*[2];
    p[0] = new std::string[2];
    p[1] = new std::string[2];
    p[0][0] = "solverA";
    p[0][1] = "argsA";
    p[1][0] = "solverB";
    p[1][1] = "argsB";

    std::string d = "instances/sat_lib_harder/";
    std::string f = "sets/instance_set_6.txt";
    Combinator c (p, d, f, true, true, 2, 100);
}
int main(){
    test_combinator();
    return 0;
}
