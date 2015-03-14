#!/bin/bash
#
# Runs the benchmarks multiple times,
# and writes the logs.
#
RUNS=$1
SOLVERS=$2
LOG_DIR=$3
INSTANCES=$4
BENCHMARK=$5

# Runs the benchmark for every solver, for
# a given number of runs.
for i in $(seq 1 $RUNS)
do
    # Runs the benchmark for a solver, and appends the sum of sys and user
    # times to a logfile for that solver.
    for i in $(seq 1 $SOLVERS)
    do
        LOG="${LOG_DIR}benchmark_$i.txt"
        TIME=`/usr/bin/time --portability python2 sat_combinator.py \
        --instance-file ${INSTANCES} --benchmark ${BENCHMARK} \
        --solve-all --select-solver $i |& grep -oP '(?<=real )[0-9]*.[0-9]*'`
        echo "$TIME" >> ${LOG}
    done
done
rm *.arff
rm classify_*
