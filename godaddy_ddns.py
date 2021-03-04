#!/usr/bin/env python3
#
# Update GoDaddy DNS "A" Record.
#
# usage: godaddy_ddns.py [-h] [--version] [--ip IP] [--key KEY]
#                        [--secret SECRET] [--ttl TTL] [--force]
#                        hostname
#
# positional arguments:
#   hostname         DNS fully-qualified host name with an 'A' record.  If the hostname consists of only a domain name
#                    (i.e., it contains only one period), the record for '@' is updated.
#
# optional arguments:
#   -h, --help       show this help message and exit
#   --version        show program's version number and exit
#   --ip IP          DNS Address (defaults to public WAN address from https://checkip.amazonaws.com/)
#   --key KEY        GoDaddy production key
#   --secret SECRET  GoDaddy production secret
#   --ttl TTL        DNS TTL.
#   --force          force update of GoDaddy DNS record even if DNS query indicates that record is already correct
#
# GoDaddy customers can obtain values for the KEY and SECRET arguments by creating a production key at
# https://developer.godaddy.com/keys/.
#
# Note that command line arguments may be specified in a FILE, one to a line, by instead giving
# the argument "%FILE".  For security reasons, it is particularly recommended to supply the
# KEY and SECRET arguments in such a file, rather than directly on the command line:
#
# Create a file named, e.g., `godaddy-ddns.config` with the content:
#   MY.FULLY.QUALIFIED.HOSTNAME.COM
#   --key
#   MY-KEY-FROM-GODADDY
#   --secret
#   MY-SECRET-FROM-GODADDY
#
# Then just invoke `godaddy-ddns %godaddy-ddns.config`

prog='godaddy-ddns'
version='0.4'
author='Carl Edman (CarlEdman@gmail.com)'

import sys, json, argparse, socket

if sys.version_info > (3,):
  from urllib.request import urlopen, Request
  from urllib.error import URLError, HTTPError
else:
  from urllib2 import urlopen, Request
  from urllib2 import URLError, HTTPError

parser = argparse.ArgumentParser(description='Update GoDaddy DNS "A" Record.', fromfile_prefix_chars='%', epilog= \
'''GoDaddy customers can obtain values for the KEY and SECRET arguments by creating a production key at
https://developer.godaddy.com/keys/.

Note that command line arguments may be specified in a FILE, one to a line, by instead giving
the argument "%FILE".  For security reasons, it is particularly recommended to supply the
KEY and SECRET arguments in such a file, rather than directly on the command line.''')

parser.add_argument('--version', action='version',
  version='{} {}'.format(prog, version))

parser.add_argument('hostname', type=str,
  help='DNS fully-qualified host name with an A record.  If the hostname consists of only a domain name (i.e., it contains only one period), the record for @ is updated.')

parser.add_argument('--ip', type=str, default=None,
  help='IPv4 address to write to DNS record (defaults to public WAN address from https://checkip.amazonaws.com/)')

parser.add_argument('--key', type=str, default='',
  help='GoDaddy production key')

parser.add_argument('--secret', type=str, default='',
  help='GoDaddy production secret')

parser.add_argument('--ttl', type=int, default=3600,
  help='DNS TTL.')

parser.add_argument('--force', type=bool, default=False,
  help='force update of GoDaddy DNS record even if DNS query indicates that record is already correct.')

args = parser.parse_args()

def main():
  hostnames = args.hostname.split('.')
  if len(hostnames)<2:
    msg = 'Hostname "{}" is not a fully-qualified host name of form "HOST.DOMAIN.TOP".'.format(args.hostname)
    raise Exception(msg)
  elif len(hostnames)<3:
    hostnames.insert(0,'@')

  if not args.ip:
    try:
      with urlopen(Request("https://checkip.amazonaws.com/", headers={'User-Agent': 'Mozilla'})) as f: resp=f.read()
      if sys.version_info > (3,): resp = resp.decode('utf-8')
      args.ip = resp.strip()
    except URLError:
      msg = 'Unable to automatically obtain IP address from https://checkip.amazonaws.com/.'
      raise Exception(msg)
  
  ipslist = args.ip.split(",")
  for ipsiter in ipslist:
    ips = ipsiter.split('.')
    if len(ips)!=4 or \
      not ips[0].isdigit() or not ips[1].isdigit() or not ips[2].isdigit() or not ips[3].isdigit() or \
      int(ips[0])>255 or int(ips[1])>255 or int(ips[2])>255 or int(ips[3])>255:
      msg = '"{}" is not valid IP address.'.format(ips)
      raise Exception(msg)

  if not args.force and len(ipslist)==1:
    try:
      dnsaddr = socket.gethostbyname(args.hostname)
      if ipslist[0] == dnsaddr:
        msg = '{} already has IP address {}.'.format(args.hostname, dnsaddr)
        raise Exception(msg)
    except:
      pass
             
  url = 'https://api.godaddy.com/v1/domains/{}/records/A/{}'.format('.'.join(hostnames[1:]),hostnames[0])
  data = json.dumps([ { "data": ip, "ttl": args.ttl, "name": hostnames[0], "type": "A" } for ip in  ipslist])
  if sys.version_info > (3,):  data = data.encode('utf-8')
  req = Request(url, method='PUT', data=data)

  req.add_header("Content-Type","application/json")
  req.add_header("Accept","application/json")
  if args.key and args.secret:
    req.add_header("Authorization", "sso-key {}:{}".format(args.key,args.secret))

  try:
    with urlopen(req) as f: resp = f.read()
    if sys.version_info > (3,):  resp = resp.decode('utf-8')
    # resp = json.loads(resp)
  except HTTPError as e:
    if e.code==400:
      msg = 'Unable to set IP address: GoDaddy API URL ({}) was malformed.'.format(req.full_url)
    elif e.code==401:
      if args.key and args.secret:
        msg = '''Unable to set IP address: --key or --secret option incorrect.
Correct values can be obtained from from https://developer.godaddy.com/keys/ and are ideally placed in a % file.'''
      else:
        msg = '''Unable to set IP address: --key or --secret option missing.
Correct values can be obtained from from https://developer.godaddy.com/keys/ and are ideally placed in a % file.'''
    elif e.code==403:
        msg = '''Unable to set IP address: customer identified by --key and --secret options denied permission.
Correct values can be obtained from from https://developer.godaddy.com/keys/ and are ideally placed in a % file.'''
    elif e.code==404:
        msg = 'Unable to set IP address: {} not found at GoDaddy.'.format(args.hostname)
    elif e.code==422:
        msg = 'Unable to set IP address: "{}" has invalid domain or lacks A record.'.format(args.hostname)
    elif e.code==429:
        msg = 'Unable to set IP address: too many requests to GoDaddy within brief period.'
    elif e.code==503:
        msg = 'Unable to set IP address: "{}" is unavailable.'.format(args.hostname)
    else:
      msg = 'Unable to set IP address: GoDaddy API failure because "{}".'.format(e.reason)
    raise Exception(msg)
  except URLError as e:
    msg = 'Unable to set IP address: GoDaddy API failure because "{}".'.format(e.reason)
    raise Exception(msg)

  print('IP address for {} set to {}.'.format(args.hostname,args.ip))

if __name__ == '__main__':
  main()
