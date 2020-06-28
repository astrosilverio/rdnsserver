NULL_BYTE = (0).to_bytes(1,'little')
POINTER_INDICATOR = b'\xc0'

def parse_dns_packet(packet):
    parsed_packet = parse_packet_headers(packet)

    if parsed_packet['question_count'] > 0:
        query_summary, global_offset = parse_query_section(packet)
        parsed_packet.update(query_summary)

    if parsed_packet['resolved_record_count'] > 0:
        answer_summary, global_offset = parse_resource_record_section(packet, global_offset)
        parsed_packet.update(answer_summary)

    if parsed_packet['authority_count'] > 0:
        authority_summary, global_offset = parse_resource_record_section(packet, global_offset)
        parsed_packet.update(authority_summary)

    if parsed_packet['additional_resource_count'] > 0:
        additional_summary, _ = parse_resource_record_section(packet, global_offset)
        parsed_packet.update(additional_summary)

    print("Transaction ID: {}".format(parsed_packet['transaction_id']))
    print("Domain: {}".format(parsed_packet['domain']))

    return parsed_packet


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
    section_data = packet[12:]
    query_name = section_data.split(NULL_BYTE)[0]
    domains = parse_name(query_name)
    # calculate the position of QTYPE in original packet by adding the first 13 bytes + length byte + 1
    section_offset = len(query_name) + 1
    query_type = int(section_data[section_offset:section_offset+2].hex(), 16)
    section_offset += 2
    query_class = int(section_data[section_offset:section_offset+2].hex(), 16)
    section_offset += 2

    query_summary = {
        'domain': domains,
        'qtype': query_type,
        'qclass': query_class,
    }

    return query_summary, section_offset+12


def parse_name(name_bytes):
    """Returns a list of domains, TLD on the end."""
    name_bytes = bytearray(name_bytes)
    domains = list()
    while name_bytes:
        domain_length = name_bytes.pop(0) # this is magically an int!
        domains.append(bytes(name_bytes[:domain_length]))
        name_bytes = name_bytes[domain_length:]

    return domains


def parse_resource_record_section(packet, offset):
    section_data = packet[offset:]
    indicator = int(section_data[0:2].hex(), 16)
    # the name is at another location if the first two bits are "11"
    if indicator >> 14 == 3:
        location = indicator ^ 49152
        previous_mention = packet[location:]
        name_segment = previous_mention.split(NULL_BYTE)[0]
        name = parse_name(name_segment)
        section_offset = 2
    else:
        name_segment = section_data.split(NULL_BYTE)[0]
        name = parse_name(name_segment)
        section_offset = len(name_segment) + 1

    rtype = int(section_data[section_offset:section_offset+2].hex(), 16)
    section_offset += 2
    rclass = int(section_data[section_offset:section_offset+2].hex(), 16)
    section_offset += 2
    ttl = int.from_bytes(section_data[section_offset:section_offset+4], byteorder='big', signed=False)
    section_offset += 4
    rdlength = int.from_bytes(section_data[section_offset:section_offset+2], byteorder='big', signed=False)
    section_offset += 2
    rdata = section_data[section_offset:section_offset+rdlength]
    section_offset += rdlength

    record_section_summary = {
        'name': name,
        'type': rtype,
        'class': rclass,
        'ttl': ttl,
        'rdlength': rdlength,
        'rdata': rdata,
    }

    # resolve the A record into an IP
    if rtype == 1 and rdlength == 4:
        ip_segments = [str(b) for b in rdata]
        ip = '.'.join(ip_segments)
        record_section_summary['ip'] = ip

    return record_section_summary, offset + section_offset
