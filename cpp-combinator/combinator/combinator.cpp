#include "../lib/solver.h"
#include <stdio.h>

Combinator::Combinator(std::string** new_solver_values,
                       std::string new_instances_dir,
                       std::string new_instance_file,
                       bool new_debug_lvl1,
                       bool new_debug_lvl2,
                       int new_solvers_length){
    solvers_length = new_solvers_length;
    debug_lvl1 = new_debug_lvl1;
    debug_lvl2 = new_debug_lvl2;

    solvers = new Solvers[solvers_length];

}

int main(){
    Solver s (0, "test_name", "test_cmd",
              "test_args", true, " ");
    printf("name: %s\n", s.get_name().c_str());
    printf("time_to_solve: %f\n", s.solve("test_instance"));
    printf("id: %d\n", s.get_id());
    InstanceBenchmark b = s.benchmark("test_instance", 10);
    printf("instance_name: %s\n", b.get_instance_name().c_str());
    double* results = b.get_values();
    for(int i = 0; i < 10; i++){
        printf("results[%d]=%f\n", i, results[i]);
    }
    return 0;
}
