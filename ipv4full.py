import sys
import fileinput
import getopt

from ipv4seq import numipv4
from ipv4holes import getholes
from prefixin import *

USAGE_MSG = """
Get IPv4 prefixes from a list
(c) POWERNET ISP 2016

Usage:
    ipv4full.py [-a|l|s] [-p] [-n] [-d] <file>

Options:
    -a|--all        Show prefixes, holes and special (default, prefer)
    -l|--hole       Only holes
    -s|--summary    Only summary of prefixes
    -p|--special    Without special
    -n|--as_path    Show AS_PATH
    -d|--prepend    Without prepend +|-|*, only with -l or -s

Input file format is A.B.C.D/X,PATH in each line
"""


def main(opt_all=False, opt_hole=False, opt_summary=False, opt_special=False, opt_aspath=False, opt_prepend=False):

    ipstack = []
    prefix_spec_i = 0

    opt_list = "alspd"
    lopt_list = ("all", "hole", "summary", "special", "aspath", "prepend")

    input_flow_name = "-"

    err_id = 0

    def prefix_out((netunion), lp, i, opt_special=False, opt_prepend=False, opt_aspath=False):
        for net in netunion:
            prefixes, i = prefix_spec(net, i)
            for p in prefixes:
                if p in PREFIX_SPEC:
                    if not opt_special:
                        sids = '*'
                    else:
                        continue
                else:
                    sids = lp

                if opt_prepend:
                    sids = ""

                print ("{}{}/{}{}".format(sids, numipv4(p[0]), p[1], ", " + p[2] if opt_aspath else ""))

        return i

    try:
        opts, args = getopt.getopt(sys.argv[1:], opt_list, lopt_list)

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

        if len(args) > 0:
            input_flow_name = args[-1]

        for line in fileinput.input(input_flow_name):

            rline = line.rstrip()

            prefix = ipv4num(rline)

            if not prefix:
                print "Invalid prefix '{}'".format(rline)
                err_id = 1
                break

            if prefix[1] > PREFIX_MAX:
                continue

            prefix = inprefix_spec(prefix, prefix_spec_i)

            holes, netunion, ipstack[:] = getholes(prefix, ipstack)

            if opt_summary or opt_all:
                prefix_spec_i = prefix_out(netunion,"+",prefix_spec_i,
                                                          opt_special, opt_prepend, opt_aspath)

            if opt_hole or opt_all:
                prefix_spec_i = prefix_out(holes, "-", prefix_spec_i,
                                                          opt_special, opt_prepend, opt_aspath)

    except IOError:
        print ("Input read error in '{}'".format(input_flow_name))
        err_id = 2
    except getopt.GetoptError:
        print (USAGE_MSG)
        err_id = 3
    finally:
        fileinput.close()

    if not err_id:
        if opt_summary or opt_all:
            prefix_out(ipstack, "+", prefix_spec_i, opt_special, opt_prepend, opt_aspath)
    else:
        exit(err_id)

if __name__ == '__main__':
    main()
