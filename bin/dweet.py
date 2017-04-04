#! /usr/bin/env /usr/bin/python

import httplib
import json
import sys
import subprocess
import getopt
from pprint import pprint
from ast import  literal_eval

SCHEMA = 'https://'
SERVER = 'dweet.io'
POST_URL = '/dweet/for/'
FOLLOW_URL = '/follow/'
NAME = 'poorman-server-discovery'


def get_ifconfig():
    co = subprocess.Popen(['/sbin/ifconfig'], stdout=subprocess.PIPE)
    iface_blocks = [block for block in co.stdout.read().split('\n\n') if block]
    ips = {}
    for block in iface_blocks:
        name = block.split()[0]
        ip = next((line.strip().split(':')[1].split(' ')[0]
                   for line in block.split('\n') if 'inet addr:' in line), None)
        if ip and name != 'lo':
            ips[name] = ip
    return ips


try:
    opts, args = getopt.getopt(sys.argv[1:], "c:h:np:d")
except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)

cluster = None
host = None
dry_run = False
send_net_cfg = False
data = {}
for opt, val in opts:
    if opt == '-t':
        cluster = val
    elif opt == '-h':
        host = val
    elif opt == '-n':
        send_net_cfg = True
    elif opt == '-p':
        if ':' in val:
            k,v = val.split(':')
            try:
                data[k] = literal_eval(v)
            except SyntaxError:
                data[k] = v
        else:
            data[val] = None
    elif opt == '-d':
        dry_run = True

if host is None:
    print 'Host ( -h ) is no optional'
    sys.exit(2)

if send_net_cfg:
    data.update(get_ifconfig())

if cluster:
    name = '-'.join((NAME, cluster, host))
else:
    name = '-'.join((NAME, host))
print 'Report to %s' % SCHEMA + SCHEMA + POST_URL + name

if not dry_run:
    h = httplib.HTTPSConnection(SERVER)
    headers = {'Content-type': 'application/json'}
    h.request('POST', POST_URL + name, json.dumps(data), headers)
    r = h.getresponse()
    if r.status == 200:
        print 'Ok'
        print 'Follow link %s' % SCHEMA + SERVER + FOLLOW_URL + name
    else:
        print 'HTTP error %s' % r.status

pprint(data)
