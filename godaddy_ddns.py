#!/usr/bin/env python
#
# GoDaddy DDNS script.
#
# usage:
#   godaddy_ddns.py XXXX
#

prog='godaddy-ddns'
version='0.1'
author='Carl Edman (CarlEdman@gmail.com)'

from urllib.request import urlopen, Request
from urllib.parse import urlparse, urlunparse, urlencode

import json, sys, argparse, logging

parser = argparse.ArgumentParser(description='Update GoDaddy DNS "A" Record.', fromfile_prefix_chars='@')

parser.add_argument('--version', action='version',
  version='{} {}'.format(prog, version))

parser.add_argument('hostname', type=str,
  help='GoDaddy DNS fully-qualified host name')

parser.add_argument('--ip', type=str, default=None,
  help='GoDaddy DNS Address (defaults to public WAN address from http://ipv4.icanhazip.com/)')

parser.add_argument('--key', type=str, default='',
  help='''GoDaddy production key from https://developer.godaddy.com/keys/
Recommended to be pulled from @file, rather than given on command line''')

parser.add_argument('--secret', type=str, default='',
  help='''GoDaddy production secret from https://developer.godaddy.com/keys/
Recommended to be pulled from @file, rather than given on command line''')

parser.add_argument('--ttl', type=int, default=3600 , help='GoDaddy DNS TTL.')
args = parser.parse_args()

def main():
  hostnames = args.hostname.split('.')
  
  if len(hostnames)<3:
    msg = 'Hostname "{}" is not a fully-qualified host name of form "HOST.DOMAIN.TOP".'.format(args.hostname)
    raise Exception(msg)
  
  if not args.ip:
    with urlopen("http://ipv4.icanhazip.com/") as f:
      args.ip=f.read().decode('utf-8').strip()
  
  ips = args.ip.split('.')
  if len(ips)!=4 or
    not ips[0].isdigit() or not ips[1].isdigit() or not ips[2].isdigit() or not ips[3].isdigit() or 
    int(ips[0])>255 or int(ips[1])>255 or int(ips[2])>255 or int(ips[3])>255):
    msg = 'IP address "{}" is not valid.'.format(args.ip)
    raise Exception(msg)

  url = 'https://api.godaddy.com/v1/domains/{}/records/A/{}'.format(hostnames[0],'.'.join(hostnames[1:]))
  data = json.dumps([ { "data": args.ip, "ttl": args.ttl, "name": hostnames[0], "type": "A" } ]).encode('utf-8')
  req = Request(url, method='PUT', data=data)

  req.add_header("Content-Type","application/json")
  req.add_header("Accept","application/json")
  if args.key and args.secret:
    req.add_header("Authorization", "sso-key {}:{}".format(args.key,args.secret))
  else:
    msg = 'Failure to provide both GoDaddy key and secret.
  These can be obtained from https://developer.godaddy.com/keys/ and are ideally placed in a @ file.'
    warnings.warn(msg)

  with urlopen(req) as f:
    resp = f.read().decode('utf-8')
    code = f.getcode()
  
  if code==200:
    print('Successfully changed GoDaddy IP address for "{}" to "{}".'.format(args.hostnames,args.ip)
  else:
    msg = 'Failure to set GoDaddy A record (code={},response={})'.format(code,resp)
    raise Exception(msg)
  
if __name__ == '__main__':
  main()
