import socket
import json

SERVER_IP = '127.0.0.1'
SERVER_PORT = 20001
BUFFER_SIZE = 1024 # huge shrug here, may have to adjust after figuring out what packets should look like

ROOT_SERVERS_FILE = 'root_servers.json'

def parse_request(request_packet):
    # bytes 0&1 are transaction ID
    # bytes 2&3 are flags
    # bytes 4&5 are the count of questions
    # bytes 6&7 are the count of RRs i.e. IPs
    # bytes 8&9 are the count of authority records
    # bytes 10&11 are the count of additional records
    # byte 11 is either a pointer or the length of the first subdomain
    # the next N bytes are the subdomain
    # the byte after is the length of the TLD
    # the next N bytes are the TLD
    tx_id = int(request_packet[0:2].hex(), 16)
    flags = int(request_packet[2:4].hex(), 16)
    question_count = int(request_packet[4:6].hex(), 16)
    resolved_record_count = int(request_packet[6:8].hex(), 16)
    authority_count = int(request_packet[8:10].hex(), 16)
    additional_resource_count = int(request_packet[10:12].hex(), 16)
    subdomain_length = int(request_packet[12:13].hex(), 16)
    end_of_subdomain = 13+subdomain_length
    subdomain = request_packet[13:end_of_subdomain].decode('utf-8')
    tld_length = int(request_packet[end_of_subdomain:end_of_subdomain+1].hex(), 16)
    end_of_tld = end_of_subdomain+1+tld_length
    tld = request_packet[end_of_subdomain+1:end_of_tld].decode('utf-8')

    request_summary = {
        'transaction_id': tx_id,
        'flags': flags,
        'question_count': question_count,
        'resolved_record_count': resolved_record_count,
        'authority_count': authority_count,
        'additional_resource_count': additional_resource_count,
        'domain': '.'.join([subdomain, tld]),
    }

    print("Transaction ID: {}".format(request_summary['transaction_id']))
    print("Domain: {}".format(request_summary['domain']))

    return request_summary


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

    with open(ROOT_SERVERS_FILE, 'r') as roots:
        root_servers = json.loads(roots.read())

    cache = {'roots': root_servers, 'TLDs': {}, 'SLDs': {}}

    while True:
        # do an echo
        request = server.recvfrom(BUFFER_SIZE)
        message = request[0]
        address = request[1]
        parse_request(message)

        server.sendto(str.encode("thanks for your attention"), address)
