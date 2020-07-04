def domains_to_fqdn(domains):
    """Changes a list of domains arranged in descending order
    into an FQDN.

    ex. ['.', 'com', 'google', 'mail'] -> 'mail.google.com'
    """
    working_domain_list = domains.copy()
    if working_domain_list[0] == '.':
        working_domain_list.pop(0)

    working_domain_list.reverse()
    return '.'.join(working_domain_list)


def fqdn_to_domains(fqdn):
    """Changes an FQDN to a list of domains arranged
    in descending order, including the root domain.

    ex. 'mail.google.com' -> ['.', 'com', 'google', 'mail']
    """
    domains = fqdn.split('.')
    domains.append('.')
    domains.reverse()
    return domains
