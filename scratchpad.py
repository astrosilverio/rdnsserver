def recursively_look_up_domains(cache, domains):
    cache_domains = domains.copy()
    a_record, traversed_domains, ns = traverse_cache(cache, cache_domains)

    untraversed_domains = domains.copy()
    untraversed_domains = remove_traversed_domains(untraversed_domains, traversed_domains)

    if a_record:
        fqdn = build_fqdn_from_reverse_domain_list(traversed_domains)
        return fqdn, a_record

    else:
        domains_for_fqdn = traversed_domains.copy()
        domains_for_fqdn.append(untraversed_domains[0])
        fqdn = build_fqdn_from_reverse_domain_list(domains_for_fqdn)
        domains_for_fqdn.reverse()
        record = fetch_dns_result(fqdn, ns)
        update_cache(cache, domains_for_fqdn, record)
        return recursively_look_up_domains(cache, domains)


def traverse_cache(cache, domains, traversed=None, ns=None):
    """Still slightly pseudocode.
    Takes a full cache, a list of domains, and optionally a list of traversed domains.
    Returns:
        - str | None:  an IP
        - list: the domains it went through, including the last step
        - str: IP of lowest level NS (currently always element 0 bc too lazy to import random)
    """
    if not traversed:
        traversed = list()

    desired_record_type = 'subdomains'
    if len(domains) == 1:
        desired_record_type = 'a'

    current_domain = domains.pop(0)
    cache = cache.get(current_domain)

    if not cache:
        return None, traversed, ns

    lower_level_ns = cache.get('ns')
    if lower_level_ns:
        ns = lower_level_ns[0]

    cache = cache.get(desired_record_type)

    if not cache:
        return None, traversed, ns

    traversed.append(current_domain)
    if isinstance(cache, str):
        return cache, traversed, ns
    else:
        return traverse_cache(cache, domains, traversed=traversed, ns=ns)


def build_fqdn_from_reverse_domain_list(domains):
    domains.reverse()
    return '.'.join(domains)


def fetch_dns_result(fqdn, ns):
    assert ns == '4.4.4.4'
    return {
        'name': 'recurse.com',
        'type': 'A',
        'rdata': '33.33.33.33'
    }


def update_cache(cache, domains, record):
    current_domain = domains.pop(0)
    while len(domains) > 0:
        cache = cache.get(current_domain)
        cache = cache.get('subdomains')
        current_domain = domains.pop(0)

    cache[current_domain] = dict()
    cache[current_domain]['subdomains'] = dict()
    cache[current_domain]['ns'] = list()

    if record['type'] == 'A':
        cache[current_domain]['a'] = record['rdata']
    elif record['type'] == 'NS':
        cache[current_domain]['ns'].append(record['rdata'])


def remove_traversed_domains(domains, traversed_domains):
    for _ in traversed_domains:
        if domains[0] in traversed_domains:
            domains.pop(0)
    return domains
