from ipv4seq import subnets, ipaddrcount, ipv4num, issubnet, numipv4

PREFIX_MAX = 24
PREFIX_SPEC = (ipv4num("0.0.0.0/8"),
               ipv4num("10.0.0.0/8"),
               ipv4num("100.64.0.0/10"),
               ipv4num("127.0.0.0/8"),
               ipv4num("169.254.0.0/16"),
               ipv4num("172.16.0.0/12"),
               ipv4num("192.0.0.0/24"),
               ipv4num("192.0.2.0/24"),
               ipv4num("192.31.196.0/24"),
               ipv4num("192.52.193.0/24"),
               ipv4num("192.88.99.0/24"),
               ipv4num("192.168.0.0/16"),
               ipv4num("192.175.48.0/24"),
               ipv4num("198.18.0.0/15"),
               ipv4num("198.51.100.0/24"),
               ipv4num("203.0.113.0/24"),
               ipv4num("224.0.0.0/3"),)


def netsub((net_s), (net_list)):

    _netsub = []

    if net_s[0] < net_list[0][0]:
        _netsub = subnets(net_s[0], net_list[0][0])

    i = 0
    while i < len(net_list)-1:
        _netsub = _netsub + [net_list[i]] + subnets(net_list[i][0]+ipaddrcount(net_list[i][1]), net_list[i+1][0])
        i += 1

    _netsub = _netsub + [net_list[-1]] + subnets(net_list[-1][0] + ipaddrcount(net_list[-1][1]),
                                                 net_s[0] + ipaddrcount(net_s[1]))

    return _netsub


def prefix_spec(prefix, i):

    prefixes = []

    if prefix != PREFIX_SPEC[i]:

        while i < len(PREFIX_SPEC) and prefix[0] > PREFIX_SPEC[i][0]:
            if not issubnet(PREFIX_SPEC[i], prefix):
                i += 1
            else:
                break

        if issubnet(prefix, PREFIX_SPEC[i]):
            prefix_sub = [PREFIX_SPEC[i]]
            i += 1
            while i < len(PREFIX_SPEC) and issubnet(prefix, PREFIX_SPEC[i]):
                prefix_sub.append(PREFIX_SPEC[i])
                i += 1

            prefixes = prefixes + netsub(prefix, prefix_sub)

        elif not issubnet(PREFIX_SPEC[i], prefix):
            prefixes.append(prefix)

    else:
        prefixes = [prefix]
        i += 1

    return prefixes, i
