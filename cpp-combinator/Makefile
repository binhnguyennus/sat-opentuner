CC=g++
CFLAGS=-Wall -O3 -std=c++11
LIBDIR=./lib
COMDIR=./combinator

all: combinator
clean:
	rm $(COMDIR)/combinator $(COMDIR)/*.o $(LIBDIR)/*.o
	
combinator: $(COMDIR)/combinator.o $(LIBDIR)/solver.o
	$(CC) $(CFLAGS) $(COMDIR)/combinator.cpp $(LIBDIR)/solver.cpp -o $(COMDIR)/combinator
