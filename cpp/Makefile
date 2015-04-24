CC=g++
CFLAGS=-Wall -O3 -std=c++11
LIBDIR=./lib
COMDIR=./combinator

all: combinator.o solver.o combinator
clean:
	rm $(COMDIR)/combinator $(COMDIR)/*.o $(LIBDIR)/*.o

combinator.o: $(COMDIR)/combinator.cpp
	$(CC) $(CFLAGS) -c $(COMDIR)/combinator.cpp -o $(COMDIR)/combinator.o

solver.o: $(LIBDIR)/solver.cpp
	$(CC) $(CFLAGS) -c $(LIBDIR)/solver.cpp -o $(LIBDIR)/solver.o

combinator: $(COMDIR)/combinator.o $(LIBDIR)/solver.o
	$(CC) $(CFLAGS) -o $(COMDIR)/combinator $(COMDIR)/combinator.o $(LIBDIR)/solver.o
