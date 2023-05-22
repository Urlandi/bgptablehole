# -*- coding: utf-8 -*-
"""
Prefix processing procedures
"""

from ipv4seq import *


def getholes(prefix, ipstack, opt_g=False):

    holes = []
    netunion = []

    while len(ipstack):
        cur_prefix = ipstack.pop()
        sum_prefix = netsum(cur_prefix, prefix, False)
        if len(sum_prefix) and opt_g:
            prefix = sum_prefix
            continue
        elif issubnet(cur_prefix, prefix, False):
            prefix = cur_prefix
            break
        elif isseq(cur_prefix, prefix) and opt_g:
            if prefix[1] <= cur_prefix[1]:
                netunion.extend(ipstack)
                netunion.append(cur_prefix)
                ipstack[:] = []
                break
            else:
                ipstack.append(cur_prefix)
                break
        else:
            for gapprefix, mask, aspath in subnets(cur_prefix[0] + ipaddrcount(cur_prefix[1]), prefix[0]):
                holes.append((gapprefix, mask, aspath))
            netunion.extend(ipstack)
            netunion.append(cur_prefix)
            ipstack[:] = []
            break

    ipstack.append(prefix)
    return holes, netunion, ipstack
