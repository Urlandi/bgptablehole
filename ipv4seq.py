ADDR_LEN = 32
ASN_MAX = 18446744073709551616L

def ipaddrcount(masklen):
    return 1 << (ADDR_LEN - masklen)


def ipmask(masklen):
    return (1 << ADDR_LEN) - ipaddrcount(masklen)


def ipv4num(address):

    addrnet = 0
    addrmask = (1 << ADDR_LEN) - 1

    addr, prefas = address.split('/')
    octets = addr.split('.')

    try:
        preflen,asn = prefas.split(',', 1)

    except ValueError:
        preflen = prefas
        asn = 0

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

        addrnet &= addrmask

        asnum = int(asn)
        if ASN_MAX < asnum < 1:
            asnum = 0

    except ValueError:
        return 0

    return addrnet, prefn, asnum


def numipv4(address):
    try:
        return "{}.{}.{}.{}".format(address >> 24, (address >> 16) & 0xff, (address >> 8) & 0xff, (address & 0xff))
    except ValueError:
        return 0


def isseq((net_s), (net_e)):
    try:
        if net_s > net_e:
            return False

        return net_s[0] + ipaddrcount(net_s[1]) == net_e[0]

    except TypeError:
        return False


def issubnet((net_s), (net_e)):
    try:
        if net_s > net_e:
            return False

        return net_s[0] + ipaddrcount(net_s[1]) > net_e[0]

    except TypeError:
        return False


def netsum((net_s), (net_e)):
    try:
        if net_s > net_e:
            return 0, 0

        if ((net_s[1] == net_e[1]) and (net_s[1] > 1) and
                (net_s[0] & ipmask(net_s[1] - 1) == (net_s[0])) and isseq(net_s, net_e)):
            return net_s[0], net_s[1] - 1
        else:
            return 0, 0

    except TypeError:
        return 0, 0

def subnets(addr_s, addr_e):
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
            _subnets.append([cur_addr_s, i])
            cur_addr_s = cur_addr_s + ipaddrcount(i)

    return _subnets


def netsub((net_s), (net_e)):

    if net_s[0] < net_e[0]:
        _netsub = subnets(net_s[0], net_e[0]) + [net_e] + subnets(net_e[0]+ipaddrcount(net_e[1]), net_s[0]+ipaddrcount(net_s[1]))
    else:
        _netsub = [net_e] + subnets(net_e[0]+ipaddrcount(net_e[1]), net_s[0]+ipaddrcount(net_s[1]))

    return _netsub
