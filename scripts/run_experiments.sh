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

cd combinator
for i in $(seq 1 $RUNS)
do
    python sat_tuning.py --no-dups --stop-after=${TIME} \
    --logdir=${LOG_DIR} \
    --bestlog=final_config_commands \
    --log-best-data \
    -i=${INSTANCE_NUMBER} \
    --instance-set=${INSTANCE_SET} \
    --parallelism=${THREADS} \
    --results-log-detail=${LOG_DIR}logall.txt \
    --results-log=${LOG_DIR}logbest.txt \
    --technique=test2
    #--seed-configuration=${LOG_DIR}seed.json
done

rm *.arff
rm classify_*
rm cp_*
rm model*
cd -
