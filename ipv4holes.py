from ipv4seq import *


def getholes(prefix, (ipstack)):

    holes = []
    netunion = []

    while len(ipstack):
        cur_prefix = ipstack.pop()
        sum_prefix = netsum(cur_prefix, prefix)
        if sum_prefix[0] and prefix[2] == cur_prefix[2] == 0:
            prefix = (sum_prefix[0], sum_prefix[1], 0,)
            continue
        elif issubnet(cur_prefix, prefix) and prefix[2] == cur_prefix[2]:
            prefix = cur_prefix
            break
        elif isseq(cur_prefix, prefix) and prefix[2] == cur_prefix[2] == 0:
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
