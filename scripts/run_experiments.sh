#! /bin/bash
# Runs a given number of experiments and
# writes the logs.
#
LOG_DIR=$1
TIME=$2
THREADS=$3
INSTANCE_DIR=$4
INSTANCE_SET=$5
INSTANCE_NUMBER=$6
CHUNKS=$7
RUNS=$8
BENCH_RUNS=$9
CONFIG_NAME='final_config_commands'

function clean {
    rm *.arff
    rm classify_*
    rm cp_*
    rm model*
}

cd combinator
for i in $(seq 1 $RUNS)
do
    mkdir ${LOG_DIR}/run_${i}
    python tuner.py --no-dups --stop-after=${TIME} \
    --logdir=${LOG_DIR}/run_${i}/ \
    --bestlog=${CONFIG_NAME} \
    --log-best-data \
    -i=${INSTANCE_NUMBER} \
    -f=${INSTANCE_SET} \
    -id=${INSTANCE_DIR} \
    --chunk-number=${CHUNKS} \
    --parallelism=${THREADS} \
    --results-log-detail=${LOG_DIR}/run_${i}/logall.txt \
    --results-log=${LOG_DIR}/run_${i}/logbest.txt
    --technique=test2
    --seed-configuration=${LOG_DIR}/seed.json
    echo `../scripts/from_file_benchmark.sh ${BENCH_RUNS} \
          ${LOG_DIR}/run_${i}/ \
          ${CONFIG_NAME}`

    rm -r opentuner.*
    clean
done

clean
cd -
