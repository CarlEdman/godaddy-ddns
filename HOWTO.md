The following instructions were quickly thrown together in response to a github request.  They should give a more newbie (or perhaps more accurately, at-least intermediate-user) friendly description of how to use this script.

The godaddy-ddns enables you to point a hostname within a GoDaddy registered domain to automatically point to a potentially changing IP address.  This is particularly useful if your ISP occasionally reassigns your IP address, but you want to give access to some services under a fixed host name.

What you will need are:

1. A GoDaddy-registered domain.  I assume you already have that.  Let's call it bar.com.

2. An A record under your domain for your home IP.  Let's give it the name foo, so in the end you'll be able to access the IP address of your home as foo.bar.com.  You can create that A record under DNS Management at the GoDaddy web site.  Setting the TTL (time to live) to the default of 1 hour is fine, but you may want to reduce it to the minimum while you experiment with the set up.  Give it a dummy IP address.

3. Your GoDaddy API Key and Secret.  Go to https://developer.godaddy.com/keys and create a new API Key and Secret and note them down somewhere.  In particular, the secret appears to be unrecoverable if you lose it.  I'll call them KEY and SECRET below.

4. A device to run the godaddy-ddns script on.  Anything on your home network that can run Python 3 will be fine.  I run it directly on my OpenWRT router, which has some advantages, but requires a relatively powerful and customized router.

5. Once you have all that, install the godaddy-ddns on your device and create a config file with the following content:
```
foo.bar.com
--key
KEY
--secret
SECRET
```
You'll of course insert the appropriate values for your host/domain/key/secret.  The line breaks in the config file are necessary.

6. Now you can automatically update the external IP address of your home network by running
`/path/to/godaddy_ddns.py %/path/to/config`

One of the advantages of running the script on your router is that you can then configure the router to run the script automatically whenever the router the reboots and/or the public IP address changes, but how exactly to do that depends on your router.  Otherwise just run it periodically from anywhere within your network.

7. Test that your record was updated properly, e.g., by running
`nslookup foo.bar.com`
After the script runs successfully it should point to your home network.  If there is some screwup, the wrong value may be cached by up to the TTL you gave above, so even if you make a correction it won't show up for that period of time.  That is the reason I suggested setting the TTL low until you are sure you got it right.
