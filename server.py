import socket
import json

from parser import parse_dns_packet


SERVER_IP = '127.0.0.1'
SERVER_PORT = 20001
BUFFER_SIZE = 1024 # huge shrug here, may have to adjust after figuring out what packets should look like

with open('root_servers.json', 'r') as roots:
    ROOT_SERVERS = json.loads(roots.read())

cache = {}

def look_up_domain(domain):
    result = cache.get(domain)
    if result:
        return result
    else:
        fetch_result(domain)


def fetch_result(domain):
    pass


def process_dns_server_response(response):
    # update that cache
    pass


def format_response(dns_result):
    # what does dig expect back ???
    pass


if __name__ == '__main__':
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind((SERVER_IP, SERVER_PORT))

    while True:
        # do an echo
        request = server.recvfrom(BUFFER_SIZE)
        message = request[0]
        address = request[1]
        parse_dns_packet(message)

        server.sendto(str.encode("thanks for your attention"), address)
