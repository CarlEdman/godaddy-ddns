# godaddy-ddns

Introduction
------------
A script for dynamically updating a GoDaddy DNS record. I use GoDaddy to host DNS for a domain and I wanted to point an A record in that domain to a host who's IP address changes occasionally. GoDaddy has an API to do this, so this happened.  This package, in particular this README.MD, is inspired by the equivalent for CloudFlare offered by [thatjpk](https://github.com/thatjpk/cloudflare-ddns).

Dependencies
------------
This program was written and tested using Python 3, so you'll need:

 - Python (`opkg install python3-light`):
 - Codecs (`opkg install python3-codecs`)
 - Email (`opkg install python3-email`)
 - OpenSSL (`opkg install python3-openssl`)
 - CA Certificates (`opkg install ca-bundle`)

The program may also work under Python 2.7 by changing python3 to python in the first line, but this configuration has not
been tested.

Usage
-----
Invoke the program like this:

     godaddy_ddns.py [-h] [--version] [--ip IP] [--key KEY] [--secret SECRET] [--ttl TTL] hostname

     positional arguments:

     hostname         DNS fully-qualified host name with an 'A' record.  If the hostname consists of only a domain name
                      (i.e., it contains only one period), the record for '@' is updated.

     optional arguments:

     -h, --help       show this help message and exit

     --version        show program's version number and exit

     --ip IP          DNS Address (defaults to public WAN address from http://ipv4.icanhazip.com/)

     --key KEY        GoDaddy production key

     --secret SECRET  GoDaddy production secret

     --ttl TTL        DNS TTL.

GoDaddy customers can obtain values for the KEY and SECRET arguments by creating a production key at https://developer.godaddy.com/keys/.

Note that command line arguments may be specified in a FILE, one to a line, by instead giving the argument "%FILE".  For security reasons, it is particularly recommended to supply the KEY and SECRET arguments in such a file, rather than directly on the command line:

Create a file named, e.g., `godaddy-ddns.config` with the content:

     MY.FULLY.QUALIFIED.HOSTNAME.COM
     --key
     MY-KEY-FROM-GODADDY
     --secret
     MY-SECRET-FROM-GODADDY

Then just invoke `godaddy-ddns %godaddy-ddns.config`

Credits and Thanks
------------------
 - [thatjpk](https://github.com/thatjpk/cloudflare-ddns) for providing an example of this type of script.
 - [GoDaddy](https://www.godaddy.com/) for having an [API](https://developer.godaddy.com/).
 - [icanhazip.com](http://icanhazip.com/) for making grabbing your public IP
    from a script super easy.
 - [dhowdy](https://github.com/dhowdy) for supplying a fix to problem with updating root DNS record.
