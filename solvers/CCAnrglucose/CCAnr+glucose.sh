#!/bin/bash

if [ "x$1" = "x" ]; then
	echo "c Usage: ./CCAnr+glucose.sh <instance> <seed> <sls_cutoff_time>"
	exit 1
fi


sls_cutoff=$3

echo "c start CCAnr"
./solvers/CCAnrglucose/CCAnr $1 $2 ${sls_cutoff}
R=$?

if [ $R != 0 ]; then
	echo "c start glucose"
	./solvers/CCAnrglucose/glucose $1
fi

