# godaddy-ddns

Introduction
------------
A script for dynamically updating a GoDaddy DNS record. I use GoDaddy to host DNS for a domain and I wanted to point an A record in that domain to a host who's IP address changes occasionally. GoDaddy has an API to do this, so this happened.  This package, in particular this README.MD, is inspired by the equivalent for CloudFlare offered by [thatjpk](https://github.com/thatjpk/cloudflare-ddns).

Dependencies
------------
You'll need:

 - Python (`opkg install python-light`):
 - Logging (`pip install python-logging`)
 - OpenSSL (`pip install python-openssl`)

Usage
-----
XXX

Credits and Thanks
------------------
 - [thatjpk](https://github.com/thatjpk/cloudflare-ddns) for providing an example of this type of script.
 - [GoDaddy](https://www.godaddy.com/) for having an [API](https://developer.godaddy.com/).
 - [icanhazip.com](http://icanhazip.com/) for making grabbing your public IP
    from a script super easy.
