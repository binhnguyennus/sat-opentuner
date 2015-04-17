CC=g++
CFLAGS=-Wall -O3 -std=c++11
LIBDIR=./lib

all: instance-benchmark, solver, combinator
clean:
	rm instance-benchmark, solver, combinator
	
instance-benchmark: $(LIBDIR)/InstanceBenchmark.cpp
	$(CC) $(CFLAGS) $(LIBDIR)/InstanceBenchmark.cpp -o instance-benchmark

solver: $(LIBDIR)/Solver.cpp $(LIBDIR)/InstanceBenchmark.cpp
	$(CC) $(CFLAGS) $(LIBDIR)/Solver.cpp $(LIBDIR)/InstanceBenchmark.cpp -o solver
