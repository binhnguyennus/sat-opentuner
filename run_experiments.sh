#! /usr/bin/zsh
# Runs a given number of experiments and
# writes the logs.
#

LOG_DIR=$1

TIME=$2
RUNS=$3

for i in {0..$RUNS}
do
    zsh -c "python2 sat_tuning.py --no-dups --stop-after="${TIME}" >>& "${LOG_DIR}${TIME}"_"$i".txt"
done
