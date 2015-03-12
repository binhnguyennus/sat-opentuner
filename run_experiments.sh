#! /bin/bash
# Runs a given number of experiments and
# writes the logs.
#
LOG_DIR=$1
TIME=$2
THREADS=$3
INSTANCE_SET=$4
INSTANCE_NUMBER=$5
RUNS=$6

for i in $(seq 1 $RUNS)
do
    python sat_tuning.py --no-dups --stop-after=${TIME} \
    --parallelism=${THREADS} \ 
    --results-log-detail=${LOG_DIR}logall.txt \ 
    --results-log=${LOG_DIR}logbest.txt \
    --instance_set=${INSTANCE_SET} \
    --i=${INSTANCE_NUMBER} \
    --logdir=${LOG_DIR} \ 
    --bestlog=final_config_commands \
    --log-best-data
    #--seed-configuration=${LOG_DIR}seed.json
    rm *.arff
    rm classify_*
done
