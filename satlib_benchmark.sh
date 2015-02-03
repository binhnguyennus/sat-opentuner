#! /usr/bin/bash
#
# Runs the benchmarks multiple times,
# and writes the logs.
#
RUNS=$1
SOLVERS=$2
LOG_DIR=$3

# Runs the benchmark for every solver, for
# a given number of runs.
for i in $(seq 1 $RUNS)
do
    # Runs the benchmark for a solver, and appends the sum of sys and user
    # times to a logfile for that solver.
    for i in $(seq 1 $SOLVERS)
    do
        TMP="${LOG_DIR}benchmark_$i"
        /usr/bin/time --portability python2 sat_combinator.py \
        --instance-file instance_set_3.txt --benchmark instances/sat_lib/ \
        --solve-all --select-solver $i &> $TMP
        USER_T=`grep -oP '(?<=user )[0-9]*.[0-9]*' ${TMP}`
        SYS_T=`grep -oP '(?<=sys )[0-9]*.[0-9]*' ${TMP}`
        SUM=$(awk "BEGIN{print $USER_T + $SYS_T}")
        echo "sum $SUM" >> ${TMP}.txt
        rm $TMP
    done
done
