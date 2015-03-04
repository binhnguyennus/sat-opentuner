#! /bin/bash
# Runs the solutions on a given file,
# for a given number of times,
# and writes the logs.
RUNS=$1
FILE_PATH=$2
FILE=$3

for i in $(seq 1 $RUNS)
do
    LOG="${FILE_PATH}/benchmark.txt"
    TIME=`/usr/bin/time --portability python2 sat_combinator.py \
    --instance-file instance_set_3.txt --benchmark instances/sat_lib/ \
    --solve-all --select-solver $i |& grep -oP '(?<=real )[0-9]*.[0-9]*'`
    bash ${FILE_PATH}/${FILE}
    echo "$TIME" >> ${LOG}
done
rm *.arff
rm classify*
