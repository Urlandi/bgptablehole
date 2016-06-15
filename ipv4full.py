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

    for net in netunion:
        print ("+{}/{}".format(numipv4(net[0]), net[1]))

    for hole in holes:
        print ("-{}/{}".format(numipv4(hole[0]), hole[1]))

for net in ipstack:
    print ("+{}/{}".format(numipv4(net[0]), net[1]))