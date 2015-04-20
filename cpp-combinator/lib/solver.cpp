#include "solver.h"

InstanceBenchmark::InstanceBenchmark(){};

InstanceBenchmark::InstanceBenchmark(std::string new_instance,
                                     std::string new_solver,
                                     double* new_values){
    solver   = new_solver;
    instance = new_instance;
    values   = new_values;
    median   = calc_median();
    mean     = calc_mean();
    stddev   = calc_stddev();
}
std::string InstanceBenchmark::get_instance_name(){
    return instance;
}
std::string InstanceBenchmark::get_solver_name(){
    return solver;
}
double InstanceBenchmark::get_mean(){
    return mean;
}
double* InstanceBenchmark::get_values(){
    return values;
}
double InstanceBenchmark::get_median(){
    return median;
}
double InstanceBenchmark::get_stddev(){
    return stddev;
}
double InstanceBenchmark::calc_stddev(){
    return 0.0;
}
double InstanceBenchmark::calc_mean(){
    return 0.0;
}
double InstanceBenchmark::calc_median(){
    return 0.0;
}

Solver::Solver() {};

Solver::Solver(int new_id, std::string new_name, std::string new_cmd,
               std::string new_args, bool new_debug){
    name  = new_name;
    cmd   = new_cmd;
    args  = new_args;
    debug = new_debug;
    id = new_id;
    separator = " ";
    if (debug){
        printf("\nSolver Being Created:\n");
        printf("Name: \"%s\"\n", name.c_str());
        printf("Command: \"%s\"\n", cmd.c_str());
        printf("Arguments: \"%s\"\n", args.c_str());
        printf("ID: %d\n", id);
        printf("Debug: %d\n", debug);
    }
}
std::string Solver::get_name(){
    return name;
}
int Solver::get_id(){
    return id;
}
InstanceBenchmark Solver::benchmark(std::string instance, int runs){
    double results[runs];
    for(int i = 0; i < runs; i++){
        results[i] = Solver::solve(instance);
    }
    InstanceBenchmark b (instance, name, results);
    return b;
}
double Solver::solve(std::string instance){
    std::string run_cmd = cmd + separator +
                          instance + separator +
                          args;
    struct timeval end;
    struct timeval start;

    if (!(system(NULL))){
        exit(1);
    }
    if (!debug) {
        run_cmd += " 2> /dev/null";
    }
    gettimeofday(&start, NULL);
    system(run_cmd.c_str());
    gettimeofday(&end, NULL);
    return (end.tv_sec - start.tv_sec) +
           (end.tv_usec - start.tv_usec) /
            1000000.0;
}
