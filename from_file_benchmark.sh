#! /bin/bash
# Runs the solutions on a given file,
# for a given number of times,
# and writes the logs.
RUNS=$1
FILE_PATH=$2
FILE=$3

for i in $(seq 1 $RUNS)
do
    bash ${FILE_PATH}/${FILE}
    for f in ${FILE_PATH}/*.txt
    do
        USER_T=`grep -oP '(?<=user )[0-9]*.[0-9]*' ${f}`
        SYS_T=`grep -oP '(?<=sys )[0-9]*.[0-9]*' ${f}`
        SUM=$(awk "BEGIN{print $USER_T + $SYS_T}")
        echo "sum $SUM" >> ${f}.sum
        rm ${f}
    done
done
