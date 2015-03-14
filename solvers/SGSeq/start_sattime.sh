#!/bin/bash

echo "c Starting sattime"
ulimit -t 1000
./solvers/SGSeq/sattime $1 -seed $3 -nbsol 1
X=$?
exit $X
