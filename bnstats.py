#!/usr/bin/python3

"""
bnstats.py v0.2 - Bitcoin nodes stats from bitnodes.21.co
This is a free software and it comes with absolutely no warranty.
You can distribute and modify it under terms of the MIT License.
Homepage: https://github.com/codehill/bnstats

Usage:
  bnstats.py [-rt <num>] countries
  bnstats.py [-rt <num>] networks
  bnstats.py [-rt <num>] hostnames
  bnstats.py [-rt <num>] timezones
  bnstats.py [-rt <num>] useragents
  bnstats.py refresh
  bnstats.py -h, --help
  bnstats.py -v, --version

Options:
  countries                 List total nodes by country
  networks                  List total nodes by ISP
  hostnames                 List total nodes by hostname
  timezones                 List total nodes by timezone
  useragents                List total nodes by user-agent
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
from iso3166 import countries

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


def node_counter(nodes, index, top):
    """Generator for counting totals."""
    counter = {}
    for node in nodes["nodes"]:
        name = nodes["nodes"][node][index]
        if name is None or name == '':
            name = "n/a"
        counter[name] = counter.get(name, 0) + 1

    i = 0
    for name in sorted(counter, key=counter.get, reverse=True):
        yield name, counter[name]

        i += 1
        if i == top:
            break


def print_formatted(label, api_index, top):
    nodes = read_datafile()
    ts = time.localtime(nodes['timestamp'])  # get snapshopt time from JSON

    # print the table header
    print("Snapshot: {}".format(time.strftime("%Y-%m-%d %H:%M", ts)))
    print("\nNo.   {:<69}Total".format(label))
    print("-" * 80)

    total = 0
    index = 0
    for name, count in node_counter(read_datafile(), api_index, top):
        total += count
        index += 1

        if api_index == 7:  # its by countries
            country = countries.get(name, None)
            if country:
                name = country.name

        print("{:>4}  {:<68} {:>5}".format(index, name[:68], count))

    # print the table footer
    print("-" * 80)
    print("Nodes in top {:<6} {:>60}".format(top, total))
    print("Total nodes {:>68}\n".format(nodes['total_nodes']))


def print_raw(api_index, top):
    nodes = read_datafile()
    for name, count in node_counter(nodes, api_index, top):
        print("{}\t{}".format(name, count))


if __name__ == '__main__':
    args = docopt(__doc__, help=True, version='bnstats v0.1')
    top_arg = int(args['--top'])  # docopt returns 10 if not set

    if args["countries"]:
        if args["--raw"]:
            print_raw(7, top_arg)
        else:
            print_formatted("Countries", 7, top_arg)

    elif args["networks"]:
        if args["--raw"]:
            print_raw(12, top_arg)
        else:
            print_formatted("Networks", 12, top_arg)

    elif args["hostnames"]:
        if args["--raw"]:
            print_raw(5, top_arg)
        else:
            print_formatted("Hostnames", 5, top_arg)

    elif args["timezones"]:
        if args["--raw"]:
            print_raw(10, top_arg)
        else:
            print_formatted("Hostnames", 10, top_arg)

    elif args["useragents"]:
        if args["--raw"]:
            print_raw(1, top_arg)
        else:
            print_formatted("Hostnames", 1, top_arg)

    elif args["refresh"]:
        download_data()
