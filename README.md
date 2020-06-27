# Recursive DNS Server

A toy project for a workshop. Definitely don't use this to do anything real.

## Useful Docs

- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/pdf/bgnet_usl_c_1.pdf) - a general introduction to socket programming, aimed at people writing socket programs in C.
- [How DNS Works](https://howdns.works/) - comic explanation of DNS.
- [How Updating DNS Works](https://jvns.ca/blog/how-updating-dns-works/) - step-by-step explanation of how a recursive DNS server works.
- [DNS Encryption Explained](https://blog.cloudflare.com/dns-encryption-explained/) - bonus reading on DNS resolution methods that use encryption, like DNS over HTTPS.

## Helpful Commands

Stuff that's useful for debugging/testing/checking your work:

- `sudo tcpdump port 53 -w out.pcap` - uses tcpdump to start listening to all network traffic and writing to a capture file you can open in Wireshark. (You can also create a capture file from within Wireshark but this is super easy!)
- `dig @localhost -p [port] google.com` - runs dig through your local DNS server at the specified port.