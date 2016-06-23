import fileinput

from ipv4holes import getholes, numipv4
from prefixin import *

ipstack = []
prefix_spec_i = 0

try:
    for line in fileinput.input():

        rline = line.rstrip()

        prefix = ipv4num(rline)

        if not prefix:
            print "Invalid prefix '{}'".format(rline)
            exit(1)

        if prefix[1] > PREFIX_MAX:
            continue

        if issubnet(PREFIX_SPEC[prefix_spec_i], prefix):
            prefix = PREFIX_SPEC[prefix_spec_i]

        holes, netunion, ipstack[:] = getholes(prefix, ipstack)

        for net in netunion:
            prefixes, prefix_spec_i = prefix_spec(net, prefix_spec_i)
            for p in prefixes:
                if p in PREFIX_SPEC:
                    sids = '*'
                else:
                    sids = '+'
                print ("{}{}/{},{}".format(sids, numipv4(p[0]), p[1], p[2]))

        for net in holes:
            prefixes, prefix_spec_i = prefix_spec(net, prefix_spec_i)
            for p in prefixes:
                if p in PREFIX_SPEC:
                    sids = '*'
                else:
                    sids = '-'
                print ("{}{}/{},{}".format(sids, numipv4(p[0]), p[1], p[2]))


except IOError, ValueError:
    print ("Input read error.")
finally:
    fileinput.close()

for net in ipstack:
    prefixes, prefix_spec_i = prefix_spec(net, prefix_spec_i)
    for p in prefixes:
        if p in PREFIX_SPEC:
            sids = '*'
        else:
            sids = '+'
        print ("{}{}/{},{}".format(sids, numipv4(p[0]), p[1], p[2]))