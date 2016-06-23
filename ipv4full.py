import sys
import fileinput
import getopt

from ipv4holes import getholes, numipv4
from prefixin import *

USAGE_MSG = """
Get IPv4 prefixes from a list
(c) POWERNET ISP 2016

Usage:
    ipv4full.py [-a|l|s] [-p] [-n] [-d] [<file>]

Options (asn is mandatory option):
    -a|--all        Show prefixes, holes and special (default, prefer)
    -l|--hole       Only holes
    -s|--summary    Only summary of prefixes
    -p|--special    Without special
    -n|--as_path    Show AS_PATH
    -d|--prepend    Without prepend +|-|*, only with -l or -s
"""


def main(argv=sys.argv[1:]):

    ipstack = []
    prefix_spec_i = 0

    opt_list = "alspd"
    lopt_list = ("all", "hole", "summary", "special", "aspath", "prepend")

    opt_all = False
    opt_hole = False
    opt_summary = False
    opt_special = False
    opt_aspath = False
    opt_prepend = False

    try:
        opts, args = getopt.getopt(argv, opt_list, lopt_list)

        for opt, arg in opts:
            if opt in ("-a", "--all"):
                opt_all = True
            elif opt in ("-l", "--hole") and not (opt_all or opt_summary):
                opt_hole = True
            elif opt in ("-s", "--summary") and not (opt_all or opt_hole):
                opt_summary = True
            elif opt in ("-p", "--special"):
                opt_special = True
            elif opt in ("-n", "--aspath"):
                opt_aspath = True
            elif opt in ("-d", "--prepend"):
                opt_prepend = True

        if not (opt_summary or opt_hole):
            opt_all = True
            opt_prepend = False

        for line in fileinput.input(sys.argv[-1]):

            rline = line.rstrip()

            prefix = ipv4num(rline)

            if not prefix:
                print "Invalid prefix '{}'".format(rline)
                break

            if prefix[1] > PREFIX_MAX:
                continue

            if issubnet(PREFIX_SPEC[prefix_spec_i], prefix):
                prefix = PREFIX_SPEC[prefix_spec_i]

            holes, netunion, ipstack[:] = getholes(prefix, ipstack)

            if opt_summary or opt_all:
                for net in netunion:
                    prefixes, prefix_spec_i = prefix_spec(net, prefix_spec_i)
                    for p in prefixes:

                        if p in PREFIX_SPEC:
                            if not opt_special:
                                sids = '*'
                            else:
                                continue
                        else:
                            sids = '+'

                        if opt_prepend:
                            sids = ""

                        print ("{}{}/{}{}".format(sids, numipv4(p[0]), p[1], ", "+p[2] if opt_aspath else ""))

            if opt_hole or opt_all:
                for net in holes:
                    prefixes, prefix_spec_i = prefix_spec(net, prefix_spec_i)
                    for p in prefixes:

                        if p in PREFIX_SPEC:
                            if not opt_special:
                                sids = '*'
                            else:
                                continue
                        else:
                            sids = '-'

                        if opt_prepend:
                            sids = ""

                        print ("{}{}/{}".format(sids, numipv4(p[0]), p[1]))

    except IOError:
        print ("Input read error in {}".format(sys.argv[-1]))
    except getopt.GetoptError:
        print (USAGE_MSG)
    finally:
        fileinput.close()

    if opt_summary or opt_all:
        for net in ipstack:
            prefixes, prefix_spec_i = prefix_spec(net, prefix_spec_i)
            for p in prefixes:

                if p in PREFIX_SPEC:
                    if not opt_special:
                        sids = '*'
                    else:
                        continue
                else:
                    sids = '+'

                if opt_prepend:
                    sids = ""

                print ("{}{}/{}{}".format(sids, numipv4(p[0]), p[1], ", "+p[2] if opt_aspath else ""))

if __name__ == '__main__':
    main()
