#include "Solver.h"

Solver::Solver(int new_id, std::string new_name, std::string new_cmd,
               std::string new_args, bool new_debug, 
               std::string new_separator) {
    name  = new_name;
    cmd   = new_cmd;
    args  = new_args;
    debug = new_debug;
    id = new_id;
    separator = new_separator;
}
std::string Solver::get_name() {
    return name;
}
int Solver::get_id() {
    return id;
}
InstanceBenchmark Solver::benchmark(std::string instance, int runs) {
    float results[runs];
    for(int i = 0; i < runs; i++){
        results[i] = 0;
    }
    std::cout << runs << "\n";
    InstanceBenchmark b (instance, name, results);
    return b;
}
double Solver::solve(std::string instance) {
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
int main() {
    Solver s (0, "test_name", "test_cmd",
              "test_args", true, " ");
    std::printf("name: %s\n", s.get_name().c_str());
    std::printf("time_to_solve: %f\n", s.solve("test_instance"));
    std::printf("id: %d\n", s.get_id());
    InstanceBenchmark b = s.benchmark("test_instance", 10);
    std::printf("instance_name: %s\n", b.get_instance_name().c_str());
    return 0;
}
