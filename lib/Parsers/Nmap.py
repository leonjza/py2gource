#!/bin/env python

# Gource input parser
# Nmap Input
#
# 2013 Leon Jacobs
# Licensed under IDC (I don't Care) license.

import sys, random, time, re

class Parser:
    def __init__(self):    
        pass
    def parse(self):            # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")

class Nmap(Parser):
    def parse(self):

        ips = {} 

        # start non blocking input reading from stdin
        try:
            buff = ""
            while True:
                buff += sys.stdin.read(1)
                if buff.endswith("\n"):
                    line = buff[:-1]

                    # check if we have the discovered open port line
                    if "Discovered open port" in line:

                        # get the ip from the line
                        ip = re.findall( r"[0-9]+(?:\.[0-9]+){3}", line )[0]

                        # check if we have seen this ip before. if we have, get the color, else, generate one
                        if ip in ips:
                            color = ips[ip]
                        else:
                            r = lambda: random.randint(0,255)
                            ips[ip] = "%02X%02X%02X" % (r(),r(),r())
                            color = ips[ip]

                        # check if it is tcp/udp
                        if "tcp" in line:
                            protocol = "tcp"
                        elif "udp" in line:
                            protocol = "udp"


                        # get the port from the string
                        regex = re.compile("(\d+)/")
                        port = regex.findall(line)[0]

                        print "%s|nmap|A|%s/%s/%s|%s" % (int(time.time()), ip, protocol, port, color)

                    buff = ""
                    sys.stdout.flush() # flush to stdout

        except KeyboardInterrupt:
           sys.stdout.flush()
           pass