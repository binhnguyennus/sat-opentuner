#include "InstanceBenchmark.h"

InstanceBenchmark::InstanceBenchmark(std::string new_instance, 
                                     std::string new_solver,
                                     double* new_values) {
    solver   = new_solver;
    instance = new_instance;
    values   = new_values;
    median   = calc_median();
    mean     = calc_mean();
    stddev   = calc_stddev();
}
std::string InstanceBenchmark::get_instance_name() {
    return instance;
}
std::string InstanceBenchmark::get_solver_name() {
    return solver;
}
double InstanceBenchmark::get_mean() {
    return mean;
}
double* InstanceBenchmark::get_values() {
    return values;
}
double InstanceBenchmark::get_median() {
    return median;
}
double InstanceBenchmark::get_stddev() {
    return stddev;
}
double InstanceBenchmark::calc_stddev() {
    return 0.0;
}
double InstanceBenchmark::calc_mean() {
    return 0.0;
}
double InstanceBenchmark::calc_median() {
    return 0.0;
}
