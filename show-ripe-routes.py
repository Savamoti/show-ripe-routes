#!/usr/bin/env python3
"""
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
"""

import sys
import argparse
import re
import json
import requests

try:
    from netaddr import IPNetwork, cidr_merge
except ModuleNotFoundError:
    print("ERROR: netaddr library not installed.\n"
        "Install it with:\n\n"
        "pip3 install netaddr\n"
        )
    sys.exit()


def validate_asn(asn):
    """Validate Autonomous System number.

    Args:
        asn (str): AS number

    Raises:
        ValueError: String must be 2/4-byte AS(0 to 4294967295).

    Returns:
        str: validated AS number
    """
    match = re.search("^AS\d{1,6}$", asn)
    if match:
        return match.group()
    else:
        raise ValueError('String must be 2/4-byte AS(0 to 4294967295).')


def get_routes(asn, ipv4=True, ipv6=False):
    """Get route objects from RIPE database.

    Args:
      asn: The ASN you want to get the routes for.
      ipv4: If True, will return IPv4 routes. Defaults to True
      ipv6: If True, will return IPv6 routes. Defaults to False

    Returns:
      tuple: A tuple with two elements. The first element is a boolean value that indicates whether the
    function was successful or not. The second element is a string that contains the error message in
    case the function was not successful. If the function was successful, the second element is a list
    of routes.
    """
    URL = "https://rest.db.ripe.net/search.json?inverse-attribute=origin&source=RIPE&query-string="
    response = requests.get(URL + asn)
    if response.status_code != 200:
        return False, "Bad status: " + str(response.status_code)

    data = json.loads(response.content.decode("utf-8"))
    if not data.get("objects"):
        return False, "Route objects not found." 

    routes = []
    for object in data["objects"]["object"]:
        for attribute in object['attributes']['attribute']:
            if ipv4 and ipv6:
                if attribute["name"] == "route" or attribute["name"] == "route6": 
                    routes.append(attribute["value"])
            elif ipv4:
                if attribute["name"] == "route": 
                    routes.append(attribute["value"])
            elif ipv6:
                if attribute["name"] == "route6": 
                    routes.append(attribute["value"])
            else:
                return False, "At least one of the arguments must be True [ipv4|ipv6]."

    return True, routes


def aggregate_routes(routes):
    """Given a list of routes, return a list of aggregated routes

    Args:
      routes (list): A list of strings representing IP address ranges.

    Returns:
      tuple: A tuple of a boolean and a list. The boolean is True if the aggregation was successful, and False
    if it was not. The list contains the aggregated routes.
    """
    try:
        routes = [IPNetwork(route) for route in routes]
        routes = cidr_merge(routes)
        return True, [str(route) for route in routes]
    except Exception as error:
        return False, error


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description="Show all route objects of AS from RIPE database."
    )
    parser.add_argument(
        "asn",
        type=validate_asn,
        help="autonomous system number",
    )
    parser.add_argument(
        "-a",
        "--aggregate",
        action='store_true',
        help="aggregate routes",
    )
    parser.add_argument(
        "-4",
        "--ipv4",
        action='store_true',
        help="will return IPv4 routes",
    )
    parser.add_argument(
        "-6",
        "--ipv6",
        action='store_true',
        help="will return IPv6 routes",
    )
    args = parser.parse_args()

    if not args.ipv4 and not args.ipv6:
        print("WARNING: at least one of the arguments is required [--ipv4|--ipv6].")
        print(parser.print_help())
        return None

    # Get routes from RIPE database
    status, routes = get_routes(args.asn, args.ipv4, args.ipv6)
    if not status:
        print("ERROR: " + routes)
        return None

    # Aggregate routes
    if args.aggregate:
        status, routes = aggregate_routes(routes)
        if not status:
            print(routes)
            return None

    for s in routes:
        print(s)


if __name__ == "__main__":
    main()
