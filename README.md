# Solving SAT instance sets with OpenTuner

This repository contains an auto-tuner and a brute force searcher that are used to find optimal combinations of solvers for a given SAT instance set. The auto-tuner is implemented using [OpenTuner](http://opentuner.org/), a framework for program auto-tuning.

## Python

### Dependencies
* Python 2.7
* [Opentuner](http://opentuner.org/tutorial/setup/)

### Running the Brute Force Searcher

With default values:

```
$ python brute-force/brute_force.py
```

## Running the Tuner

With default values:

```
$ python combinator/tuner.py
```

###Scripts

#### Benchmarking

To benchmark all solvers using a given instance set, run:

```
$ ./scripts/benchmark.sh [RUNS] [SOLVERS] [LOG_DIR] [INSTANCE_SET] [INSTANCE_DIR]

[RUNS]: A number specifying how many times to run the solvers (sample size).
[SOLVERS], (0..7): A number specifying how many solvers to benchmark. 
[LOG_DIR]: The path to log the benchmarks.
[INSTANCE_SET]: Where to find the file that specify the instances to solve.
[INSTANCE_DIR]: Where to find the instance files.
```

#### Running the Tuner

This script runs OpenTuner to find good solver combinations for a given instance set, and logs all tuning results and the final best configuration.

```
$ ./scripts/run_experiments.sh [LOG_DIR] [TIME] [THREADS] [INSTANCE_DIR] [INSTANCE_SET] [INSTANCE_NUMBER] [CHUNKS] [RUNS] [BENCHMARK_RUNS]

[LOG_DIR]: The path to log the results.
[TIME]: The number of seconds to run OpenTuner for.
[THREADS]: Size of the OpenTuner ThreadPool.
[INSTANCE_DIR]: Where to find the instance files.
[INSTANCE_SET]: Where to find the file that specify the instances to solve.
[INSTANCE_NUMBER]: The size of the instance set.
[CHUNKS]: Number of subdivisions in the instance set.
[BENCH_RUNS]: A number specifying how many times to run OpenTuner.
[RUNS]: A number specifying how many times to run the combinations found (sample size).
```

#### Benchmarking a Configuration File

Benchmarks a configuration file created by OpenTuner:

```
$ ./scripts/from_file_benchmark.sh [RUNS] [FILE_PATH] [FILE]

[RUNS]: A number specifying how many times to run the combinations found (sample size).
[FILE_PATH]: Where to find the file.
[FILE]: The file with the combination commands.
```

## C++
