#include "Benchmark.h"

Benchmark::Benchmark(std::string new_instance, std::string new_solver, 
                     float* new_values) {
    solver   = new_solver;
    instance = new_instance;
    values   = new_values;
    median   = calc_median();
    mean     = calc_mean();
    stddev   = calc_stddev();
}
std::string Benchmark::get_instance_name() {
    return instance;
}
std::string Benchmark::get_solver_name() {
    return solver;
}
float Benchmark::get_mean() {
    return mean;
}
float* Benchmark::get_values() {
    return values;
}
float Benchmark::get_median() {
    return median;
}
float Benchmark::get_stddev() {
    return stddev;
}
float Benchmark::calc_stddev() {
    return 0.0;
}
float Benchmark::calc_mean() {
    return 0.0;
}
float Benchmark::calc_median() {
    return 0.0;
}
