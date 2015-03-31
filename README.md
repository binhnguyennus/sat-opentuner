# Solving SAT instance sets with OpenTuner
This repository contains an auto-tuner and a brute force searcher that are used to find optimal combinations 
of solvers for a given SAT instance set. The auto-tuner is implemented using [OpenTuner](http://opentuner.org/),
a framework for program auto-tuning.

### Dependencies
* Python 2.7
* [Opentuner](http://opentuner.org/tutorial/setup/)

### Benchmarking

Run:

```
$ ./scripts/benchmark.sh [RUNS] [SOLVERS] [LOG_DIR] [INSTANCE_SET] [INSTANCE_DIR]
```

Where:
* [RUNS]: A number specifying how many times to run the solvers (sample size).
* [SOLVERS], (0..7): A number specifying how many solvers to benchmark. 
* [LOG_DIR]: The path to log the benchmarks.
* [INSTANCE_SET]: Where to find the file that specify the instances to solve.
* [INSTANCE_DIR]: Where to find the instance files.

### Running the Tuner

### Running the Brute Force Searcher
