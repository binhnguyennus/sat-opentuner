CC=g++
CFLAGS=-Wall -O3 -std=c++11
LIBDIR=./lib

all: benchmark, solver, combinator
clean:
	rm benchmark, solver, combinator
	
benchmark: $(LIBDIR)/Benchmark.cpp
	$(CC) $(CFLAGS) $(LIBDIR)/Benchmark.cpp -o benchmark

solver: $(LIBDIR)/Solver.cpp $(LIBDIR)/Benchmark.cpp
	$(CC) $(CFLAGS) $(LIBDIR)/Solver.cpp $(LIBDIR)/Benchmark.cpp -o solver
