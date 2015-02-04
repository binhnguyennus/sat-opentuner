#! /bin/bash
# Runs a given number of experiments and
# writes the logs.
#
LOG_DIR=$1
TIME=$2
RUNS=$3

for i in $(seq 1 $RUNS)
do
    python2 sat_tuning.py --no-dups --stop-after=${TIME} \
        &> ${LOG_DIR}${TIME}_$i.txt
    rm *.arff
    rm classify_*
done
