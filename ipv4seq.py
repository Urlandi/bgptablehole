ADDR_LEN = 32
ASN_MAX = 18446744073709551616L


def ipaddrcount(masklen):
    return 1 << (ADDR_LEN - masklen)


def ipmask(masklen):
    return (1 << ADDR_LEN) - ipaddrcount(masklen)


def ipv4num(address):

    addrnet = 0

    try:
        addr, prefas = address.split('/')
        octets = addr.split('.')
    except ValueError:
        return 0

    try:
        preflen, aspath = prefas.split(',', 1)

    except ValueError:
        preflen = prefas
        aspath = 0

    try:
        i = 0
        for octet in reversed(octets):
            octetnum = int(octet)
            if 0 <= octetnum <= 255:
                addrnet += octetnum * (1 << i)
                i += 8

        prefn = int(preflen)
        if 1 <= prefn <= ADDR_LEN:
            addrmask = ipmask(prefn)
        else:
            return 0

        addrnet &= addrmask

    except ValueError:
        return 0

    return addrnet, prefn, aspath


def numipv4(address):
    try:
        return "{}.{}.{}.{}".format(address >> 24, (address >> 16) & 0xff, (address >> 8) & 0xff, (address & 0xff))
    except ValueError:
        return 0


def isiple((net_s), (net_e)): #net_s < net_e
    if net_s[0] < net_e[0] or ( net_s[0] == net_e[0] and net_s[1] < net_e[1]):
        return True
    else:
        return False


def isipleq((net_s), (net_e)): #net_s <= net_e
    if net_s[0] < net_e[0] or ( net_s[0] == net_e[0] and net_s[1] <= net_e[1]):
        return True
    else:
        return False


def isseq((net_s), (net_e)):
    try:
        if isipleq(net_e, net_s):
            return False

        return net_s[0] + ipaddrcount(net_s[1]) == net_e[0]

    except TypeError:
        return False


def issubnet((net_s), (net_e)):
    try:
        if isiple(net_e, net_s):
            return False

        return net_s[0] + ipaddrcount(net_s[1]) > net_e[0]

    except TypeError:
        return False


def netsum((net_s), (net_e)):
    try:
        if isipleq(net_e, net_s):
            return 0, 0

        if ((net_s[1] == net_e[1]) and (net_s[1] > 1) and
                (net_s[0] & ipmask(net_s[1] - 1) == (net_s[0])) and isseq(net_s, net_e)):
            return net_s[0], net_s[1] - 1
        else:
            return 0, 0

    except TypeError:
        return 0, 0


def subnets(addr_s, addr_e, aspath=0):
    _subnets = []

    def prefix_l(s, e):

        l = ADDR_LEN

        addr_count = e - s

        while addr_count:
            addr_count >>= 1
            l -= 1
        while (s & ipmask(l) != s) or (s + ipaddrcount(l)) > e:
            l += 1

        return l

    if addr_s < addr_e:
        cur_addr_s = addr_s

        while cur_addr_s < addr_e:
            i = prefix_l(cur_addr_s, addr_e)
            _subnets.append([cur_addr_s, i, aspath])
            cur_addr_s = cur_addr_s + ipaddrcount(i)

    return _subnets

def netsub((net_s), (net_list)):

    _netsub = []

    if net_s[0] < net_list[0][0]:
        _netsub = subnets(net_s[0], net_list[0][0], net_s[2])

    i = 0
    while i < len(net_list)-1:
        _netsub = _netsub + [net_list[i]] + \
                  subnets(net_list[i][0]+ipaddrcount(net_list[i][1]), net_list[i+1][0], net_s[2])
        i += 1

    _netsub = _netsub + [net_list[-1]] + \
              subnets(net_list[-1][0] + ipaddrcount(net_list[-1][1]), net_s[0] + ipaddrcount(net_s[1]), net_s[2])

    return _netsub