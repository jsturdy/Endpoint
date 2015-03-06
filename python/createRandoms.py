#!/bin/py

from random import *

outfile = file("randomNumbers.txt","w")

for i in range(0,20000):

#	s = "%d\t%d\n"%(randint(100000000,999999999),randint(100000000,999999999))
	s = "%d"%(randint(100000000,999999999))
	s += "\t%d"%(randint(100000000,999999999))
	s += "\t%d"%(randint(100000000,999999999))
	s += "\t%d"%(randint(100000000,999999999))
	s += "\t%d"%(randint(100000000,999999999))
	s += "\n"
	outfile.write(s)


