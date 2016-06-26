### Search non routing IP prefixes in route table

#### Execute

Run as <b>freeIPv4.py</b> \<<i>file with list of IPv4 prefixes</i>\> or <b>freeIPv4.py</b> [-a|l|s] [-p] [-n] [-d] \<file\>

Options:
<pre>
    -a|--all        Show prefixes, holes and special (default, prefer)
    -l|--hole       Only holes
    -s|--summary    Only summary of prefixes
    -p|--special    Without special
    -n|--as_path    Show AS_PATH
    -d|--prepend    Without prepend +|-|*, only with -l or -s</pre>

Returned summary of prefixes by AS_PATH (if exists) and holes between it.

Input file format is A.B.C.D/X,PATH in each line sorted by ascending. PATH and comma with it maybe not present

#### Source data

- holeroutetable.log - list of prefixes that not exist in <b>24routetable.log</b>, without [special nets](http://www.iana.org./assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml)
- 24routetable.log - list of prefixes /24 and shorter from <b>routetable.log</b>, without [special nets](http://www.iana.org./assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml)
- routetable.log - list of unique prefixes from [archive](http://archive.routeviews.org/oix-route-views/2016.04/oix-full-snapshot-2016-04-20-2200.bz2)

[There is article about this on Habrahabr](https://habrahabr.ru/post/282532/)
