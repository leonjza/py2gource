#!/bin/env python

# Gource input parser
# Main Script
#
# 2013 Leon Jacobs
# Licensed under IDC (I don't Care) license.

from optparse import OptionParser
import sys, re, time, random

# from lib import Parser
from lib.Parsers import Argus, Nmap, Postfix

parsers = { "nmap" , "argus", "postfix" }

def main():
    parser = OptionParser()
    parser.add_option("-t","--type", dest="type", help="Input type. Supported types: %s" % ", ".join(i for i in parsers))

    (options, args) = parser.parse_args()

    if options.type not in parsers or options.type == "None":
        print "ERROR: Invalid or no input type specified.\n"
        parser.print_help()
        sys.exit(1)

    if options.type == "nmap":
        Nmap.Nmap().parse()
    if options.type == "argus":
        Argus.Argus().parse()
    if options.type == "postfix":
        Postfix.Postfix().parse()

if __name__ == "__main__":
   main()
