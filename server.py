import socket

cache = dict()

server_ip = '127.0.0.1'
server_port = 20001
buffer_size = 1024 # huge shrug here, may have to adjust after figuring out what packets should look like


def parse_request(request_packet):
    # what does dig send ???? :/
    pass


def lookup_domain(domain):
    result = cache.get(domain)
    if result:
        return result


def process_dns_server_response(response):
    # update that cache
    pass


def format_response(dns_result):
    # what does dig expect back ???
    pass


if __name__ == '__main__':
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind((server_ip, server_port))

    while True:
        # do an echo
        request = server.recvfrom(buffer_size)
        message = request[0]
        address = request[1]

        server.sendto(message, address)
