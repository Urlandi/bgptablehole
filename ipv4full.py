# -*- coding: utf-8 -*-
"""
Generate prefix list from file
"""

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
    ipv4full.py [-a|l|s] [-g] [-p] [-n] [-d] <file>

Options:
    -a|--all        Show prefixes, holes and special (default, prefer)
    -l|--hole       Only holes
    -s|--summary    Only summary of prefixes
    -g|--aggregate  Allow aggregate sequences, otherwise only nested prefixes aggregated
    -p|--special    Without special
    -n|--as_path    Show AS_PATH
    -d|--prepend    Without prepend +|-|*, only with -l or -s

Input file format is A.B.C.D/X,PATH in each line
"""


def main(opt_all=False, opt_hole=False, opt_summary=False, opt_aggregate=False, opt_special=False, opt_aspath=False, opt_prepend=False):

    ipstack = []
    prefix_spec_i = 0
    prefix_asn = 0

    opt_list = "alsgpnd"
    lopt_list = ("all", "hole", "summary", "aggregate", "special", "aspath", "prepend")

    input_flow_name = "-"

    err_id = 0

    def prefix_out((netin), lp, i, a, opt_s=False, opt_p=False, opt_n=False):
        for net in netin:
            if net[2] != a:
                i = 0
            prefixes, i = prefix_spec(net, i)
            for p in prefixes:
                if p in PREFIX_SPEC:
                    if not opt_s:
                        sids = '*'
                    else:
                        continue
                else:
                    sids = lp

                if opt_p:
                    sids = ""

                print ("{}{}/{}{}".format(sids, numipv4(p[0]), p[1], ", " + str(p[2]) if opt_n else ""))

            a = net[2]

        return i,a

    try:
        opts, args = getopt.getopt(sys.argv[1:], opt_list, lopt_list)

        for opt, arg in opts:
            if opt in ("-a", "--all"):
                opt_all = True
            elif opt in ("-l", "--hole") and not (opt_all or opt_summary):
                opt_hole = True
            elif opt in ("-s", "--summary") and not (opt_all or opt_hole):
                opt_summary = True
            elif opt in ("-g", "--aggregate"):
                opt_aggregate = True
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

        # Main cycle
        for line in fileinput.input(input_flow_name):

            rline = line.strip()

            prefix = ipv4num(rline)

            if not len(prefix):
                print "Invalid prefix '{}'".format(rline)
                err_id = 1
                break

            # Filter too long mask
            if prefix[1] > PREFIX_MAX:
                continue

            if prefix_asn != prefix[2]:
                prefix_spec_i = 0

            prefix = inprefix_spec(prefix, prefix_spec_i)

            # Main executes
            holes, netunion, ipstack[:] = getholes(prefix, ipstack, opt_aggregate)

            # Print output
            if opt_summary or opt_all:
                prefix_spec_i, prefix_asn = prefix_out(netunion, "+", prefix_spec_i, prefix_asn, opt_special, opt_prepend, opt_aspath)

            if opt_hole or opt_all:
                prefix_spec_i, prefix_asn = prefix_out(holes, "-", prefix_spec_i, prefix_asn, opt_special, opt_prepend, opt_aspath)

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
            # After execute print
            prefix_out(ipstack, "+", prefix_spec_i, prefix_asn, opt_special, opt_prepend, opt_aspath)

    return err_id

if __name__ == '__main__':
    exit(main())
