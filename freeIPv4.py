import fileinput

from ipv4holes import *

ipstack = []

for line in fileinput.input():

    rline = line.rstrip()

    prefix = ipv4num(rline)

    if not prefix:
        print "Invalid prefix '{}'".format(rline)
        exit(1)

    holes, netunion, ipstack[:] = getholes(prefix, ipstack)

    for hole in holes:
        print ("{}/{}".format(numipv4(hole[0]), hole[1]))
