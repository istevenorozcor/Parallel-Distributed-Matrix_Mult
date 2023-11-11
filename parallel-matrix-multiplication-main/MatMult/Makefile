GCC = gcc
oT = -fopenmp -O3

CFLAGS = -lm

oL= Otime.c

BINDIR = ../
PROGS = $(BINDIR)MM1c $(BINDIR)MM1r

all: MM1c MM1r

clean:
	$(RM) $(PROGS)

MM1c:
	$(GCC) $(oT) $(oL) $@.c -o $(BINDIR)$@ $(CFLAGS)

MM1r:
	$(GCC) $(oT) $(oL) $@.c -o $(BINDIR)$@ $(CFLAGS)
