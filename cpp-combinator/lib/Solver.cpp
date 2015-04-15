#include "Solver.h"

Solver::Solver(std::string new_name, std::string new_cmd,
                std::string new_args, bool new_debug) {
    name  = new_name;
    cmd   = new_cmd;
    args  = new_args;
    debug = new_debug;
}
std::string Solver::get_name() {
    return name;
}
Benchmark Solver::benchmark(std::string instance, int runs) {
    float results[runs];
    for(int i = 0; i < runs; i++){
        results[i] = 0;
    }
    std::cout << runs << "\n";
    Benchmark b (instance, name, results);
    return b;
}
float Solver::solve(std::string instance) {
    if (debug) {
        std::cout << debug << "\n";
    }
    std::cout << cmd << " " << instance << "\n";
    return 0.0;
}
int main() {
    Solver s ("test_name", "test_cmd",
              "test_args", true);
    std::cout << s.get_name() << "\n";
    std::cout << s.solve("test_instance") << "\n";
    Benchmark b = s.benchmark("test_instance", 10);
    std::cout << b.get_instance_name() << "\n";
    return 0;
}
