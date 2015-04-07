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
BENCH_RUNS=$7
CONFIG_NAME='final_config_commands'

cd combinator
for i in $(seq 1 $RUNS)
do
    mkdir ${LOG_DIR}/run_${i}
    python tuner.py --no-dups --stop-after=${TIME} \
    --logdir=${LOG_DIR}/run_${i}/ \
    --bestlog=${CONFIG_NAME} \
    --log-best-data \
    -i=${INSTANCE_NUMBER} \
    --instance-set=${INSTANCE_SET} \
    --parallelism=${THREADS} \
    --results-log-detail=${LOG_DIR}/run_${i}/logall.txt \
    --results-log=${LOG_DIR}/run_${i}/logbest.txt
    #--technique=test2
    #--seed-configuration=${LOG_DIR}seed.json
    echo `../scripts/from_file_benchmark.sh ${BENCH_RUNS} \
          ${LOG_DIR}/run_${i}/ \
          ${CONFIG_NAME}`

    rm -r opentuner.*
    rm *.arff
    rm classify_*
    rm cp_*
    rm model*
done

cd -
