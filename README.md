# Recursive DNS Server

A toy project for a workshop. Definitely don't use this to do anything real.

## Useful Docs

- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/pdf/bgnet_usl_c_1.pdf) - a general introduction to socket programming, aimed at people writing socket programs in C.
- [How DNS Works](https://howdns.works/) - comic explanation of DNS.
- [How Updating DNS Works](https://jvns.ca/blog/how-updating-dns-works/) - step-by-step explanation of how a recursive DNS server works.
- [DNS Encryption Explained](https://blog.cloudflare.com/dns-encryption-explained/) - bonus reading on DNS resolution methods that use encryption, like DNS over HTTPS.

## Helpful Commands

Stuff that's useful for debugging/testing/checking your work:

- `sudo tcpdump [-i lo0] [port 53] -w out.pcap` - uses tcpdump to start listening to all network traffic and writing to a capture file you can open in Wireshark. `-i lo0` tells (BSD?) tcpdump to listen to all loopback (ie, local) traffic for when you're running your own server on localhost, and port 53 is the designated port for DNS. (You can also create a capture file from within Wireshark but this is super easy!)
- `dig @localhost -p [port] google.com` - runs dig through your local DNS server at the specified port.

## To-Do

- Right now, we assume you only pass one subdomain in because it's easier. In the future, we should grab the beginning of the message (transaction ID, flags, etc) and the end (type, class, additional records) and loop through the middle in case there are multiple subdomains (ex: mail.google.com). But right now passing something with multiple subdomains'll just fart out.