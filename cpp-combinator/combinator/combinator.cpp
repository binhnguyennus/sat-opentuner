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
    infile.close();
}
double Combinator::solve(int* combination){
    double result = 0;
    if(debug_lvl1){
        printf("Starting to solve a Combination with length %d.\n",
               combination_length);
    }
    for (int i = 0; i < combination_length; i++){
        result += solve(combination[i], i);
    }
    return result;
}
double Combinator::solve(int solver_id){
    double result = 0;
    if(debug_lvl1){
        printf("Starting to solve a set with length %d, ",
               combination_length);
        printf("using Solver %d\n", solver_id);
    }
    for (int i = 0; i < combination_length; i++){
        result += solve(solver_id, i);
    }
    return result;
}
double Combinator::solve(int solver_id, int target_id){
    return solvers[solver_id].solve(instances[target_id]);
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
    Solver s (0, "minisat", "./solvers/minisat_blbd/minisat_blbd", 
              "", true);
    printf("name: %s\n", s.get_name().c_str());
    printf("time_to_solve: %f\n",
           s.solve("instances/sat_lib_harder/uf150-0100.cnf"));
    printf("id: %d\n", s.get_id());
    InstanceBenchmark b;
    b = s.benchmark("instances/sat_lib_harder/uf150-0100.cnf", 10);
    printf("instance_name: %s\n", b.get_instance_name().c_str());
    double* results = b.get_values();
    for (int i = 0; i < 10; i++){
        printf("results[%d]=%f\n", i, results[i]);
    }
}
void test_combinator(){
    std::string** solver_names = new std::string*[7];
    for (int i = 0; i < 7; i++){
        solver_names[i] = new std::string[2];
    }
    solver_names[0][0] = "./solvers/glueSplit/glueSplit_clasp";
    solver_names[0][1] = "";

    solver_names[1][0] = "./solvers/Lingeling/lingeling -v";
    solver_names[1][1] = "";

    solver_names[2][0] = "./solvers/Lingeling/lingeling -v --druplig";
    solver_names[2][1] = "";

    solver_names[3][0] = "./solvers/Sparrow/SparrowToRiss.sh";
    solver_names[3][1] = "1 .";

    solver_names[4][0] = "./solvers/minisat_blbd/minisat_blbd";
    solver_names[4][1] = "";

    solver_names[5][0] = "./solvers/SGSeq/SGSeq.sh";
    solver_names[5][1] = "";

    solver_names[6][0] = "./cryptominisat/cryptominisat";
    solver_names[6][1] = "";

    std::string d = "instances/sat_lib_harder/";
    std::string f = "sets/instance_set_6.txt";

    Combinator c (solver_names, d, f, true, false, 2, 100);
    printf("Solving with \"0\": %f\n", c.solve(0));
    printf("Solving with \"1\": %f\n", c.solve(1));
}
int main(int argc, char* argv[]){
    int SOLVER_LENGTH = 7;
    std::string** solver_names = new std::string*[SOLVER_LENGTH];
    for (int i = 0; i < SOLVER_LENGTH; i++){
        solver_names[i] = new std::string[2];
    }
    solver_names[0][0] = "./solvers/glueSplit/glueSplit_clasp";
    solver_names[0][1] = "";

    solver_names[1][0] = "./solvers/Lingeling/lingeling -v";
    solver_names[1][1] = "";

    solver_names[2][0] = "./solvers/Lingeling/lingeling -v --druplig";
    solver_names[2][1] = "";

    solver_names[3][0] = "./solvers/Sparrow/SparrowToRiss.sh";
    solver_names[3][1] = "1 .";

    solver_names[4][0] = "./solvers/minisat_blbd/minisat_blbd";
    solver_names[4][1] = "";

    solver_names[5][0] = "./solvers/SGSeq/SGSeq.sh";
    solver_names[5][1] = "";

    solver_names[6][0] = "./cryptominisat/cryptominisat";
    solver_names[6][1] = "";

    std::string instances_dir = "instances/sat_lib_harder/";
    std::string instance_file = "sets/instance_set_6.txt";

    Combinator c (solver_names, instances_dir, instance_file, true, 
                  false, SOLVER_LENGTH, 100);
    printf("Solving with \"0\": %f\n", c.solve(0));
    printf("Solving with \"3\": %f\n", c.solve(3));
    return 0;
}
