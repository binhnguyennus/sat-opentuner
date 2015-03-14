#!/bin/bash

if [ "x$1" = "x" ]; then
  echo "USAGE: SGS.sh INSTANCE -s SEED -tmp TMPDIR"
  exit 1
fi
./solvers/SGSeq/start_sattime.sh $1 -seed $3
X=$?
if [ $X != 10 ]; then
  echo "c Starting glucose"
  ./solvers/SGSeq/glucose $1
fi
