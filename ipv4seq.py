# -*- coding: utf-8 -*-
"""
Utilities for manipulating IP (v4)
"""


ADDR_LEN = 32                       # IPv4 max mask
ASN_MAX = 18446744073709551616L     # ASN 32bit max number


def ipaddrcount(masklen):
    """Return address count by mask length"""

    return 1 << (ADDR_LEN - masklen)


def ipmask(masklen):
    """Return bit mask by mask length"""

    return (1 << ADDR_LEN) - ipaddrcount(masklen)


def ipv4num(address):
    """
    Convert IPv4 address to list

    Arg is string as "A.B.C.D/Y,ASPATH", where
    A,B,C,D,Y is valid numbers in address
    "ASPATH" - various string

    "ASPATH" with comma may be absent

    Return is list of 3 items:

    0. digitized IPv4 net
    1. digitized mask length
    2. as is "ASPATH" or 0 if absent

    or 0 if errors occur

    Some exceptions handled
    """

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
    """
    Convert digitized IPv4 net to string

    Arg is number from 0 to 2^32 (IPv4 address)

    Return string "A.B.C.D"
    or 0 if errors occur

    Some exceptions handled
    """

    try:
        return "{}.{}.{}.{}".format(address >> 24, (address >> 16) & 0xff, (address >> 8) & 0xff, (address & 0xff))

    except ValueError:
        return 0


def isiple((net_s), (net_e)):
    """
    True if arg1 < arg2

    arg1, arg2 is valid IPv4 address list from ipv4num procedure

    True if:
    arg1:192.0.2.0/Any, arg2:192.0.2.1-255/Any
    arg1:192.0.2.0/24, arg2:192.0.2.0/25-32

    False else
    """

    if net_s[0] < net_e[0] or (net_s[0] == net_e[0] and net_s[1] < net_e[1]):
        return True

    return False


def isipleq((net_s), (net_e)):
    """
    True if arg1 <= arg2

    arg1, arg2 is valid IPv4 address list from ipv4num procedure

    True if:
    arg1:192.0.2.0/Any, arg2:192.0.2.1-255/Any
    arg1:192.0.2.0/24, arg2:192.0.2.0/24-32

    False else
    """

    if net_s[0] < net_e[0] or (net_s[0] == net_e[0] and net_s[1] <= net_e[1]):
        return True

    return False


def isseq((net_s), (net_e)):
    """
    Return True if net in arg2 begin immediately after net in arg1

    arg1, arg2 is valid IPv4 address list from ipv4num procedure

    True if:
    arg1:192.0.2.4/30, arg2:192.0.2.8/30
    """

    try:
        if isiple(net_s, net_e):
            return net_s[0] + ipaddrcount(net_s[1]) == net_e[0]

    except TypeError:
        return False

    return False


def issubnet((net_s), (net_e)):
    """
    Return True if net in arg2 is included in net in arg1

    arg1, arg2 is valid IPv4 address list from ipv4num procedure

    Return True if:
    arg1:192.0.2.0/30, arg2:192.0.2.2/31
    arg1:192.0.2.0/30, arg2:192.0.2.0/30
    """

    try:
        if isipleq(net_s, net_e):
            return net_s[0] + ipaddrcount(net_s[1]) > net_e[0]

    except TypeError:
        return False

    return False


def netsum((net_s), (net_e)):
    """
    Return new net as sum of net in arg1 with net in arg2

    arg1, arg2 is valid IPv4 address list from ipv4num procedure

    arg1 < arg2

    Return 192.0.2.0/29 if:
    arg1:192.0.2.0/30, arg2:192.0.2.4/30

    Return empty list when unable to sum
    """

    _netsum = []

    try:
        if isiple(net_s, net_e):
            if (net_s[1] == net_e[1]) and \
                    (net_s[1] > 1) and \
                    (net_s[0] & ipmask(net_s[1] - 1) == (net_s[0])) and \
                    isseq(net_s, net_e):
                _netsum = [net_s[0], net_s[1] - 1]

    except TypeError:
        return _netsum

    return _netsum


def subnets(addr_s, addr_e, aspath=0):
    """
    Return list of nets between arg1 and arg2

    arg1, arg2 is valid digitized IPv4 address

    arg1 in range, arg2 out range

    ASPATH must coincide in arg1 and arg2

    arg1 < arg2, otherwise return an empty list
    """

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
    """
    Return list of subnets in arg1 where subnets in arg2 must be present visibly

    arg1 is valid IPv4 address list from ipv4num procedure

    arg2 is valid list where items is valid IPv4 address list from ipv4num procedure
    """

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
