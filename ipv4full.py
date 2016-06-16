import fileinput

from ipv4holes import ipv4num, getholes, numipv4, issubnet, netsub
from prefixin import *

ipstack = []
prefix_spec_i = 0

for line in fileinput.input():

    rline = line.rstrip()

    prefix = ipv4num(rline)

    if not prefix:
        print "Invalid prefix '{}'".format(rline)
        exit(1)

    if prefix[1] > PREFIX_MAX:
        continue

    prefixes = [prefix]

    prefix_spec = ipv4num(PREFIX_SPEC[prefix_spec_i])

    while prefix > prefix_spec and not issubnet(prefix_spec, prefix):
        prefix_spec_i += 1
        prefix_spec = ipv4num(PREFIX_SPEC[prefix_spec_i])

    if issubnet(prefix, prefix_spec):
        prefixes = netsub(prefix, prefix_spec)
    elif issubnet(prefix_spec, prefix):
        continue

    for cur_prefix in prefixes:
        holes, netunion, ipstack[:] = getholes(cur_prefix, ipstack)

        for net in netunion:
            print ("+{}/{}".format(numipv4(net[0]), net[1]))

        for hole in holes:
            print ("-{}/{}".format(numipv4(hole[0]), hole[1]))

for net in ipstack:
    print ("+{}/{}".format(numipv4(net[0]), net[1]))