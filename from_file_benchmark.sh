#! /bin/bash
# Runs the solutions on a given file,
# for a given number of times,
# and writes the logs.
RUNS=$1
FILE_PATH=$2
FILE=$3

for i in $(seq 1 $RUNS)
do
    COUNTER=0
    while read line; do
        LOG="${FILE_PATH}/benchmark_${COUNTER}.txt"
        bash -c "${line} |& grep -oP '(?<=real )[0-9]*.[0-9]*' >> ${LOG}"
        COUNTER=$((COUNTER+1))
    done < "${FILE_PATH}/${FILE}"
done
rm *.arff
rm classify*
