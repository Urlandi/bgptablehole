### Search non routing IP prefixes in route table

Run as <b>freeIPv4.py</b> \<<i>file with list of IPv4 prefixes</i>\>

- holeroutetable.log - list of prefixes that not exist in <b>24routetable.log</b>, without [special nets](http://www.iana.org./assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml)
- 24routetable.log - list of prefixes /24 and shorter from <b>routetable.log</b>, without [special nets](http://www.iana.org./assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml)
- routetable.log - list of unique prefixes from [archive](http://archive.routeviews.org/oix-route-views/2016.04/oix-full-snapshot-2016-04-20-2200.bz2)

[There is article about this on Habrahabr](https://habrahabr.ru/post/282532/)
