#ifndef __INSTANCEBENCHMARK_H_INCLUDED__
#define __INSTANCEBENCHMARK_H_INCLUDED__

#include <string>

class InstanceBenchmark {
    std::string instance;
    std::string solver;
    double median, mean, stddev;
    double* values;

    double calc_median();
    double calc_mean();
    double calc_stddev();

    public:
        double* get_values();
        double get_median();
        double get_mean();
        double get_stddev();

        std::string get_solver_name();
        std::string get_instance_name();
        InstanceBenchmark(std::string, std::string, double*);
};
#endif
