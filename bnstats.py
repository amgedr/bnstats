#!/usr/bin/python3

"""
bnstats.py v0.1 - Bitcoin nodes stats from bitnodes.21.co
This is a free software and it comes with absolutely no warranty.
You can distribute and modify it under terms of the MIT License.
Homepage: https://github.com/codehill/bnstats

Usage:
  bnstats.py [-rt <num>] countries
  bnstats.py [-rt <num>] networks
  bnstats.py refresh
  bnstats.py -h, --help
  bnstats.py -v, --version

Options:
  countries                 List total nodes by countries
  networks                  List total nodes by ISPs
  refresh                   Redownload the data from bitnodes.21.co
  -t <num>, --top <num>     Number of rows returned [default: 10]
  -r, --raw                 Return raw output
  -h, --help                Show this help screen
  -v, --version             Print the version number
"""

import os
import sys
import json
import time
import requests
from docopt import docopt

SNAPSHOT_URL = "https://bitnodes.21.co/api/v1/snapshots/latest/"
DATA_FILE = 'bnstats.json'


def download_data():
    """Download most recent data from bitnodes.21.co to current directory"""
    try:
        print('Downloading latest snapshot...')
        nodes_resp = requests.get(SNAPSHOT_URL)

        print('Saving data to {} in current directory...'.format(DATA_FILE))
        with open(DATA_FILE, 'w', encoding='utf8') as file:
            file.write(nodes_resp.text)

        print('Done.')

    except Exception as ex:
        print(ex)


def read_datafile():
    """Read data file if exists and download it if it doesn't"""
    try:
        # if data file does not exist then download data and create file
        if not os.path.exists(DATA_FILE):
            download_data()

        with open(DATA_FILE, encoding='utf8') as file:
            nodes = json.load(file)

        return nodes

    except PermissionError:
        print("Could'nt write to {} or to current directory".format(DATA_FILE))
        sys.exit(1)


def by_county(nodes, top):
    """Iterator for countries and their total nodes."""
    countries = {}
    for node in nodes["nodes"]:
        country = nodes["nodes"][node][7]
        if country is not None and country != "":
            countries[country] = countries.get(country, 0) + 1
        else:
            countries["  "] = countries.get(country, 0) + 1

    i = 0
    for country in sorted(countries, key=countries.get, reverse=True):
        yield country, countries[country]

        i += 1
        if i == top:
            break


def by_country_formatted(nodes, top):
    """Prints countries and their total nodes."""
    ts = time.localtime(nodes["timestamp"])  # get snapshopt time from JSON

    print("Snapshot: {}".format(time.strftime("%Y-%m-%d %H:%M", ts)))
    print("\nNo.   Country{}Total".format(" " * 14))
    print("-" * 32)

    total = 0
    i = 0
    for country, count in by_county(nodes, top):
        i += 1
        total += count
        print("{:>3}   {:<5}{:>21d}".format(i, country, count))

    print("-" * 32)
    print("Nodes in top {:<6} {:>12}".format(top, total))
    print("Total nodes {:>20}\n".format(nodes["total_nodes"]))


def by_network(nodes, top):
    """Iterator for networks and their total nodes."""
    networks = {}
    for node in nodes["nodes"]:
        nw = nodes["nodes"][node][12]
        if nw is not None and nw != "":
            networks[nw] = networks.get(nw, 0) + 1
        else:
            networks["  "] = networks.get(nw, 0) + 1

    i = 0
    for nw in sorted(networks, key=networks.get, reverse=True):
        yield nw, networks[nw]

        i += 1
        if i == top:
            break


def by_network_formatted(nodes, top):
    """Print networks and their total nodes."""
    ts = time.localtime(nodes["timestamp"])  # get snapshopt time from JSON

    print("Snapshot: {}".format(time.strftime("%Y-%m-%d %H:%M", ts)))
    print("\nNo.  Network{}Total".format(" " * 63))
    print("-" * 80)

    total = 0
    i = 0
    for nw, count in by_network(nodes, top):
        i += 1
        total += count
        print("{:>3}  {:<69} {:>5}".format(i, nw[:69], count))

    print("-" * 80)
    print("Nodes in top {:<6} {:>60}".format(top, total))
    print("Total nodes {:>68}\n".format(nodes["total_nodes"]))


if __name__ == '__main__':
    args = docopt(__doc__, help=True, version='bnstats v0.1')
    top_arg = int(args['--top'])  # docopt returns 10 if not set

    if args["countries"]:
        if args["--raw"]:
            for country, cnt in by_county(read_datafile(), top_arg):
                print("{}\t{}".format(country, cnt))
        else:
            by_country_formatted(read_datafile(), top_arg)

    elif args["networks"]:
        if args["--raw"]:
            for nw, cnt in by_network(read_datafile(), top_arg):
                print("{}\t{}".format(nw, cnt))
        else:
            by_network_formatted(read_datafile(), top_arg)

    elif args["refresh"]:
        download_data()
