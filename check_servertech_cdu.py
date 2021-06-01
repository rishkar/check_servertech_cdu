#!/bin/python3

import argparse
import easysnmp
import sys

# Define constants
STECH_SNMP_PRE = "1.3.6.1.4.1.1718."
RARITAN_SNMP_PRE = "1.3.6.1.4.1.13742"
SENTRY3_CDU = 0
SENTRY4_CDU = 1
PRO3X_CDU = 2

def valid_snmp_object(snmp_value):
    return snmp_value!='NOSUCHOBJECT'

def main():
    # Define parser and arguments
    parser = argparse.ArgumentParser(description='This script runs SNMPv2c' 
                                                ' checks on any Servertech CDU' 
                                                ' to verify that it is in a'
                                                ' good state. Currently accepts'
                                                ' Servertech Sentry3, Sentry4,' 
                                                ' and PRO3X CDUs.')
    parser.add_argument('-H', '--host', type=str, required=True, 
                        help='The hostname, FQDN or IP of the Servertech CDU')
    parser.add_argument('-c', '--community', default='public', 
                        help='The (RO) SNMPv2c community string to query the'
                            ' host with. Defaults to \"public\"')
    parser.add_argument('-t', '--temp', type=int, 
                        help='Returns CRITICAL status if any installed'
                        ' temperature sensors report a temperature equal to or'
                        ' above this value. Does nothing if no temperature'
                        ' sensors are installed.')
    parser.add_argument('--timeout', default=10, type=int, 
                        help='Amount of time to wait for a response before'
                            ' calling it quits. Defaults to 10 seconds.')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Show detailed status messages')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show VERY detailed status messages. Not for the'
                            ' faint of heart.')
    args = parser.parse_args()

    # Put our args into more easy-on-the-eyes variables
    snmp_host = args.host
    snmp_community = args.community
    snmp_crit_temp = args.temp
    snmp_conn_timeout = args.timeout
    be_verbose = args.verbose
    be_debug = args.debug

    # Try to establish a connection with the SNMP host and grab a basic variable.
    # If this fails, exit immedeately.

    # Test hostname
    try:
        snmp_connection = easysnmp.Session(hostname=snmp_host, version=2, 
                                        community=snmp_community,
                                        timeout=snmp_conn_timeout)
    except easysnmp.exceptions.EasySNMPConnectionError:
        print("ERROR: Could not establish SNMP connection with the host. Is your"
            " hostname correct?")
        sys.exit(1)

    # Test SNMP community string
    try:
        snmp_connection.get("sysDescr.0")
    except easysnmp.exceptions.EasySNMPTimeoutError:
        print("ERROR: Timed out while attempting to communicate with the host. Is"
            " your SNMP community string correct?")
        sys.exit(1)

    # Find out what type our CDU is (sentry3, sentry4, or PRO3X)
    servertech_cdu_type = None
    if (valid_snmp_object(snmp_connection.get(STECH_SNMP_PRE + '3.1.1.0'))):
        servertech_cdu_type = SENTRY3_CDU
    elif (valid_snmp_object(snmp_connection.get(STECH_SNMP_PRE + '4.1.1.0'))):
        servertech_cdu_type = SENTRY4_CDU
    elif (valid_snmp_object(snmp_connection.get(RARITAN_SNMP_PRE 
                                                + '6.3.2.1.1.1'))):
        servertech_cdu_type = PRO3X_CDU

if __name__ == "__main__":
    main()
