import socket
import json

SERVER_IP = '127.0.0.1'
SERVER_PORT = 20001
BUFFER_SIZE = 1024 # huge shrug here, may have to adjust after figuring out what packets should look like
NULL_BYTE = (0).to_bytes(1,'little')

with open('root_servers.json', 'r') as roots:
    ROOT_SERVERS = json.loads(roots.read())

cache = {}


def parse_dns_packet(packet):
    headers = parse_packet_headers(packet)

    query_summary, global_offset = parse_query_section(packet[12:])

    answer_summary, global_offset = parse_resource_record_section(packet, global_offset)
    authority_summary, global_offset = parse_resource_record_section(packet, global_offset)
    additional_summary, _ = parse_resource_record_section(packet global_offset)

    print("Transaction ID: {}".format(request_summary['transaction_id']))
    print("Domain: {}".format(request_summary['domain']))

    return request_summary


def parse_packet_headers(packet):
    # bytes 0&1 are transaction ID
    # bytes 2&3 are flags
    # bytes 4&5 are the count of questions
    # bytes 6&7 are the count of RRs i.e. IPs
    # bytes 8&9 are the count of authority records
    # bytes 10&11 are the count of additional records
    tx_id = int(packet[0:2].hex(), 16)
    flags = int(packet[2:4].hex(), 16)
    question_count = int(packet[4:6].hex(), 16)
    resolved_record_count = int(packet[6:8].hex(), 16)
    authority_count = int(packet[8:10].hex(), 16)
    additional_resource_count = int(packet[10:12].hex(), 16)

    return {
        'transaction_id': tx_id,
        'flags': flags,
        'question_count': question_count,
        'resolved_record_count': resolved_record_count,
        'authority_count': authority_count,
        'additional_resource_count': additional_resource_count,
    }


def parse_query_section(packet):
    query_name = variable_data.split(NULL_BYTE)[0]
    domains = parse_query_name(query_name)
    # calculate the position of QTYPE in original packet by adding the first 12 bytes + length byte + 
    query_type_offset = len(query_name) + 1
    query_type = int(packet[query_type_offset:query_type_offset+2].hex(), 16)
    query_class = int(packet[query_type_offset+2:query_type_offset+4].hex(), 16)

    return domains, query_type, query_class, query_type_offset+4


def parse_query_name(query_name):
    """Returns a list of domains, TLD on the end."""
    query_name = bytearray(query_name)
    domains = list()
    while query_name:
        domain_length = query_name.pop(0) # this is magically an int!
        domains.append(bytes(query_name[:domain_length]))
        query_name = query_name[domain_length:]

    return domains


def parse_resource_record_section(name):
    pass


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
