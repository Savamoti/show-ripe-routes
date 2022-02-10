# show-ripe-routes

## What is it?
The script that show all route objects of AS from RIPE database

## How-To
```
$ ./show-ripe-routes.py --help
usage: show-ripe-routes.py [-h] [-a] [-4] [-6] asn

Show all route objects of AS from RIPE database.

positional arguments:
  asn              autonomous system number

optional arguments:
  -h, --help       show this help message and exit
  -a, --aggregate  aggregate routes
  -4, --ipv4       will return IPv4 routes
  -6, --ipv6       will return IPv6 routes
```

You can get aggregated IPv4 and IPv6 routes. For example - yandex:
```
$ ./show-ripe-routes.py AS13238 -4 -6 -a
5.45.192.0/18
5.255.192.0/18
37.9.64.0/18
37.140.128.0/18
77.88.0.0/18
84.252.160.0/19
87.250.224.0/19
90.156.176.0/23
93.158.128.0/18
95.108.128.0/17
141.8.128.0/18
178.154.128.0/18
185.32.187.0/24
213.180.192.0/19
2a02:6b8::/29
2a0e:fd87::/47
```
