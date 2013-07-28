#py2gource.py

##Information:
py2gource.py is a middleware script to parse input, producing output readable by Gource in the custom log format specified in the Gource wiki.

Gource is used to visualise commit history, but using this middleware and Gource's ability to accept custom input, you can do cool things like visualise Nmap scans or network activity from a Argus network monitor.

The basic idea is to take output, push it though the middleware, and then finally to Gource.  A simple, high level usage example:

`cat some_thing | python py2gource.py | gource`

**NB:** A key part for this type of _live_ input to Gource is to specify the `--realtime --log-format custom -` arguments  so that it will accept its input from *stdin* in the custom log format.

While the parser simply, well, parses, you can simulate a form of history recording of the parsed output using `tee` just before you pipe to Gource. A full usage example, which includes all the required switches for visualising a live Nmap scan:

```bash
% nmap -v 192.168.137.0/24 | python py2gource.py -t nmap | tee parsed_nmap | gource --realtime --log-format custom - -1440x900 --bloom-intensity 0.3 -e 0.2 -i 120 --title "Nmap of 192.168.137.0/24"
```

##Requires:
- python 2.x
- gource https://code.google.com/p/gource/

##Current Supported Parsers:
- Nmap (-v argument required, for now)    http://nmap.org/
- Argus   http://qosient.com/argus/

##Sample parsed Argus Output
![Sample parsed Argus Output](http://i.imgur.com/eDc3EPlh.png)

##Default Middleware Options
``` bash
% python py2gource.py
ERROR: Invalid or no input type specified.

Usage: py2gource.py [options]

Options:
  -h, --help            show this help message and exit
  -t TYPE, --type=TYPE  Input type. Supported types: nmap, argus
```

###Note
I'm guessing it will be possible to get this to work on Windows as there are Gource and Python binaries available for download. However, your on your own™ :p

##Contact
Twitter: @leonjza
