from ipv4seq import ipv4num, issubnet, netsub

PREFIX_MAX = 24

# http://www.iana.org./assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
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

        elif issubnet(PREFIX_SPEC[i], prefix):
            prefixes = [PREFIX_SPEC[i]]
        else:
            prefixes.append(prefix)

    else:
        prefixes = [prefix]

    return prefixes, i


def inprefix_spec(prefix, slice):

    for prefix_spec in PREFIX_SPEC[slice:]:
        if prefix[0] < prefix_spec[0]:
            break
        elif issubnet(prefix_spec, prefix):
            return prefix_spec

    return prefix
