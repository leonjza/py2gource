#!/bin/env python

# Gource input parser
# Argus Input
#
# 2013 Leon Jacobs
# Licensed under IDC (I don't Care) license.

import sys, random, time

class Parser:
    def __init__(self):    
        pass
    def parse(self):            # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")

class Argus(Parser):
    def parse(self):

        s_ips = {} 
        d_ips = {} 

        # start non blocking input reading from stdin
        try:
            buff = ""
            while True:
                buff += sys.stdin.read(1)
                if buff.endswith("\n"):
                    line = buff[:-1]

                    data = line.split()
                    # print(data)

                    # check if the line was the headings.
                    if data[3] != "SrcAddr":

                        # check that the line has flags or not.
                        if data[3] != "->":
                            source_data = 3
                            destination_data = 5
                        else:
                            source_data = 2
                            destination_data = 4

                        # prepare the source ip/port
                        s = data[source_data].split(".")
                        if len(s) == 5: # run this if the src port is available. things like ARP dont have src_port
                            s_ip = ".".join(s[i] for i in range(0,4))
                            s_port = s[-1]

                            # check if we have seen this ip before. if we have, get the color, else, generate one
                            if s_ip in s_ips:
                                s_color = s_ips[s_ip]
                            else:
                                r = lambda: random.randint(0,255)
                                s_ips[s_ip] = "%02X%02X%02X" % (r(),r(),r())
                                s_color = s_ips[s_ip]
                        elif len(s) == 4:
                            s_ip = s
                            s_port = "0"

                            # check if we have seen this ip before. if we have, get the color, else, generate one
                            if s_ip in s_ips:
                                s_color = s_ips[s_ip]
                            else:
                                r = lambda: random.randint(0,255)
                                s_ips[s_ip] = "%02X%02X%02X" % (r(),r(),r())
                                s_color = s_ips[s_ip]                            
                        else: #finally, if nothing can be determined
                            s_ip = "0"

                        # prepare the destination ip/port
                        d = data[destination_data].split(".")
                        # print d
                        if len(d) == 5: # run this if the dst port is available. things like ARP dont have dst_port
                            d_ip = ".".join(d[i] for i in range(0,4))
                            d_port = d[-1]

                            # check if we have seen this ip before. if we have, get the color, else, generate one
                            if d_ip in d_ips:
                                d_color = d_ips[d_ip]
                            else:
                                r = lambda: random.randint(0,255)
                                d_ips[d_ip] = "%02X%02X%02X" % (r(),r(),r())
                                d_color = d_ips[d_ip]
                        elif len(s) == 4:
                            d_ip = d
                            d_port = "0"

                            # check if we have seen this ip before. if we have, get the color, else, generate one
                            if d_ip in d_ips:
                                d_color = d_ips[s_ip]
                            else:
                                r = lambda: random.randint(0,255)
                                d_ips[d_ip] = "%02X%02X%02X" % (r(),r(),r())
                                d_color = d_ips[s_ip]                                     
                        else:
                            d_ip = "0"

                        # only print if there is valid data :)
                        if "0" != (s_ip or d_ip):
                            print "%s|%s|A|%s/%s/%s/%s/%s|%s" % (int(time.time()), s_ip, d[0], d[1], d[2], d[3], d_port, d_color)

                    buff = ""
                    sys.stdout.flush() # flush to stdout

        except KeyboardInterrupt:
           sys.stdout.flush()
           pass