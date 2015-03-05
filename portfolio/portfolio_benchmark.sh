#!/bin/bash
#
# Runs the benchmarks multiple times,
# and writes the logs.
#
RUNS=$1
SOLVERS=$2
LOG_DIR=$3
MAX_THREADS=1024

# Runs the benchmark for a solver, and appends the sum of sys and user
# times to a logfile for that solver.
for i in $(seq 1 $SOLVERS)
do
    let THREADS=1
    LOG=${LOG_DIR}benchmark_${i}.txt
    touch ${LOG}
    while [ $THREADS -le $MAX_THREADS ]; do
        TMP="${LOG_DIR}tmp_${THREADS}.txt"
        echo "${THREADS}" >> ${TMP}
        for j in $(seq 1 $RUNS)
        do
            TIME=`/usr/bin/time -p python2 sat_portfolio.py \
            --benchmark=${i} --threads=${THREADS} \
            |& grep -oP '(?<=real )[0-9]*.[0-9]*'`
            echo "${TIME}" >> ${TMP}
        done
        `paste ${LOG} ${TMP} | column -t > tmp`
        `cat tmp > ${LOG}`
        `rm ${TMP} tmp`
        let THREADS=2*THREADS
    done
done
rm *.arff classify*
