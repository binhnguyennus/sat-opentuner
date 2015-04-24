#include "../lib/solver.h"
#include "combinator.h"

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
        for (int i = 0; i < instance_set_size; i++){
            infile >> instance;
            instances[i] = dir + instance;
            if (debug_lvl1){
                printf("Instance Added: \"%s\"\n", instances[i].c_str());
            }
        }
    }
    else if (debug_lvl1){
        printf("\nError opening file: \"%s\"\n", file.c_str());
        exit(1);
    }
    infile.close();
}
void Combinator::parse_options(){
    std::ifstream infile(file.c_str());
    if (!infile.fail()){
        std::string option;
        infile >> option;
        while (!infile.eof()){
            if (option == "INSTANCE_DIR:"){
                infile >> instances_dir;
            } else if (option == "INSTANCE_FILE:"){
                infile >> instance_file;
            } else if (option == "SET_SIZE:"){
                infile >> instance_set_size;
            } else if (option == "D" || option == "D1"){
                debug_lvl1 = true;
            } else if (option == "D2"){
                debug_lvl2 = true;
            } else {
                printf("\nNo such option: \"%s\"\n", option.c_str());
                exit(1);
            }
        infile >> option;
        }
    } else {
        printf("\nError opening file: \"%s\"\n", file.c_str());
        exit(1);
    }
    infile.close();
}
void Combinator::print_configuration(){
    printf("\nLoaded the following configurations from \"%s\": \n",
           file.c_str());
    printf("Instance Directory: %s\n", instances_dir.c_str());
    printf("Instance File: %s\n", instance_file.c_str());
    printf("Instance Set Size: %d\n", instance_set_size);
}
void Combinator::load_arguments(int argc, char* argv[]){
    if (argc > 1){
        file = argv[1];
        printf("Reading configuration from \"%s\" ... ", file.c_str());
        parse_options();
        if (debug_lvl1){
            print_configuration();
        }
        printf("Done.\n");
    } else {
        printf("\nError: No configuration file.\n");
        exit(1);
    }
}
double Combinator::solve(int* combination){
    double result = 0;
    if(debug_lvl1){
        printf("\nStarting to solve a Combination with length %d.\n",
               instance_set_size);
    }
    for (int i = 0; i < instance_set_size; i++){
        result += solve(combination[i], i);
    }
    return result;
}
double Combinator::solve(int solver_id){
    double result = 0;
    if(debug_lvl1){
        printf("\nStarting to solve a set with length %d, ",
               instance_set_size);
        printf("using Solver %d:\n", solver_id);
    }
    for (int i = 0; i < instance_set_size; i++){
        result += solve(solver_id, i);
    }
    return result;
}
double Combinator::solve(int solver_id, int target_id){
    return solvers[solver_id].solve(instances[target_id]);
}
Combinator::Combinator(std::string** solver_values,
                       int new_solvers_length,
                       int argc, char* argv[]){
    solvers_length     = new_solvers_length;
    load_arguments(argc, argv);

    solvers = new Solver[solvers_length];
    instances = new std::string[instance_set_size];
    if (debug_lvl1){
        printf("\nCreating Combinator: \n");
        printf("Solvers: %d\n", solvers_length);
        printf("Combination Length: %d\n", instance_set_size);
        printf("Debug_LVL2: %d\n", debug_lvl2);
        printf("Instance File: %s\n", instance_file.c_str());
        printf("Instances Dir: %s\n", instances_dir.c_str());
        printf("\nInitializing Solver List:\n");
    }
    build_solver_list(solver_values);
    if (debug_lvl1){
        printf("\nInitializing Instance List.\n");
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

    Combinator c (solver_names, SOLVER_LENGTH, argc, argv);

    double result = c.solve(1);
    printf("Time: %3.10f\n", result);
}
