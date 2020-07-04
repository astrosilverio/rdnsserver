import unittest

from utils import domains_to_fqdn, fqdn_to_domains


class TestDomainsToFqdn(unittest.TestCase):

    def test_utils_construct_fqdn_from_domain_list(self):
        domains = ['.', 'com', 'recurse']
        fqdn = domains_to_fqdn(domains)
        self.assertEqual(fqdn, 'recurse.com')

        # Make sure scope weirdness doesn't impact parent vars
        self.assertEqual(domains, ['.', 'com', 'recurse'])

    def test_utils_construct_fqdn_from_incomplete_domain_list(self):
        domains = ['com', 'recurse']
        fqdn = domains_to_fqdn(domains)
        self.assertEqual(fqdn, 'recurse.com')

        # Make sure scope weirdness doesn't impact parent vars
        self.assertEqual(domains, ['com', 'recurse'])


class TestFqdnToDomains(unittest.TestCase):

    def test_utils_construct_domain_list_from_fqdn(self):
        fqdn = 'recurse.com'
        domains = fqdn_to_domains(fqdn)
        self.assertEqual(domains, ['.', 'com', 'recurse'])

    def test_domain_order_preserved_across_transformations(self):
        fqdn = 'recurse.com'
        domains = fqdn_to_domains(fqdn)
        new_fqdn = domains_to_fqdn(domains)
        self.assertEqual(new_fqdn, fqdn)
        new_domains = fqdn_to_domains(new_fqdn)
        self.assertEqual(new_domains, domains)
