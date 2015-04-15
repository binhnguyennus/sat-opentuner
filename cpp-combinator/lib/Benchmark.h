#ifndef __BENCHMARK_H_INCLUDED__
#define __BENCHMARK_H_INCLUDED__

#include <string>

class Benchmark {
    std::string instance;
    std::string solver;
    float median, mean, stddev;
    float* values;

    float calc_median();
    float calc_mean();
    float calc_stddev();

    public:
        float* get_values();
        float get_median();
        float get_mean();
        float get_stddev();

        std::string get_solver_name();
        std::string get_instance_name();
        Benchmark(std::string, std::string, float*);
};
#endif
