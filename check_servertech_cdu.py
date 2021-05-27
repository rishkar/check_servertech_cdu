#!/bin/python3

import argparse

# This python script does SNMP checks on the provided Servertech CDU to verify that it and any linked nodes are in a good state.

parser = argparse.ArgumentParser()
parser.add_argument('-h', '--host', type=str, required=True, help="The hostname, FQDN or IP of the Servertech CDU")
parser.add_argument('-t', '--temp', type=int)
parser.add_argument('--timeout', default=10, type=int)
parser.add_argument('-v', '--verbose')
parser.add_argument('-d', '--debug')
parser.add_argument('--help', action='help')