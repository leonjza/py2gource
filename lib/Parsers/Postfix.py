#!/bin/env python

# Gource input parser
# Nmap Input
#
# 2014 Bruce McIntyre
# Licensed under IDC (I don't Care) license.

import sys, random, time, re, datetime
from time import strftime

class Parser:
    def __init__(self):    
        pass
    def parse(self):            # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")

class Postfix(Parser):
    def parse(self):

        ips = {} 
        start_time = 0

        # start non blocking input reading from stdin
        try:
            buff = ""
            while True:
                buff += sys.stdin.read(1)
                if buff.endswith("\n"):
                    line = buff[:-1]
            
                    line_parsed = False        
                    
                    elems = line.split(': ')

                    # year
                    year = datetime.datetime.now().year

                    # get the date
                    m = re.search("(\w+)\s+(\d+) (\d+):(\d+):(\d+) .*", elems[0])
                    if m:
                        d = str(year) + " " + m.groups()[0] + " " + str(m.groups()[1]) + " " + str(m.groups()[2]) + ":" + str(m.groups()[3]) + ":" + str(m.groups()[4])

                    # put it in epoch
                    ed = datetime.datetime.strptime(d, "%Y %b %d %H:%M:%S")
                    epoch = int(ed.strftime("%s"))
                    
                    foo = {'connect': 'A', 'disconnect': 'D'}

                    # deal just with the smtpd side of things
                    if ("postfix/smtpd" in elems[0]):
                        # ignore warnings for now
                        if "warning" in elems[1]:
                            pass
                        else:
                            if "improper command pipelining after" in line:
                                pass

                            elif "lost connection after RCPT" in line:
                                pass
                            else:
                                n = re.search("(\w+) from (.*)\[(.*)\]", elems[1])
                                if n:
                                    action = n.groups()[0]
                                    host = n.groups()[1]
                                    ip = n.groups()[2]
                                    if ip in ips:
                                        s_color = ips[ip]
                                    else:
                                        r = lambda: random.randint(0,255)
                                        ips[ip] = "%02X%02X%02X" % (r(),r(),r())
                                        s_color = ips[ip]

                                    if (action == "connect"):
                                      command = "A"
                                    else:
                                      command = "D"

                                    if (ip == "unknown"):
                                        ip = 'x.x.x.x'

                                    octets = ip.split(".")

                                    print "%s|%s|%s|%s/%s/%s/%s/%s/%s|%s" % (epoch, ip, command, octets[0], octets[1], octets[2], octets[3], ed.strftime("%Y-%m-%d %H:%M"), host, s_color)
                                                        
                    buff = ""
                    sys.stdout.flush() # flush to stdout

        except KeyboardInterrupt:
           sys.stdout.flush()
           pass