#!/usr/bin/python
#author = 'mamahtehok'

import sys, argparse
import json, urllib2


#healthuri = "http://10.10.20.1/healthstatus"

#function load nginx health status page in json format
def json_load(uri):
    r = urllib2.urlopen(uri)
    data = json.load(r)
    servers = data['servers']['server']
    return servers
#function split ip:port pair
def portsplit(ipport):
    ip = ipport.split(':')
    return ip[0]

#script args define
pars = argparse.ArgumentParser();
pars.add_argument('-u', '--url', help='Url for nginx health status page in json format', required=True)
pars.add_argument('-a', '--action', help='script action - discovery or status', required=True)
pars.add_argument('-i', '--ip', help='get host status by ip')
args = pars.parse_args()


if args.action == 'discovery':
    servers = json_load(args.url)

    print "{\n"
    print "\t\"data\":[\n\n"
    first = 1
    for server in servers:
	if not first:
	   print("\t,\n")
	first = 0
        print("\t{\n\t\t\"{#IPUP}\":\""+portsplit(server['name'])+"\"\n\t}\n")
    print "\n\t]\n"
    print "}\n"

elif args.action == 'status':
    servers = json_load(args.url)
    if not args.ip:
        for server in servers:
            print(portsplit(server['name'])+": "+server['status'])
    else:
        srv = [s for s in servers if portsplit(s['name']) == args.ip]
        if srv[0]['status'] == "up":
	   print("1")
	else:
	   print("0")
