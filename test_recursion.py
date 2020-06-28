import unittest

import scratchpad


test_cache = {
'.': {
    'a': '0.0.0.0',
    'ns': ['1.1.1.1', '2.2.2.2', '3.3.3.3'],
    'subdomains': {
        'com': {
            'a': '11.11.11.11',
            'ns': ['4.4.4.4'],
            'subdomains': {
                'google': {
                    'a': '22.22.22.22',
                    'ns': [],
                    'subdomains': {},
                },
            },
        },
    },
},
}


class TestFetchingFromCache(unittest.TestCase):

    def test_fetching_an_existing_a_record(self):
        """We should get back the A record itself,
        all domains in traversed category,
        ns at level of one domain above"""
        domains = [".", "com", "google"]

        a_record, traversed_domains, ns = scratchpad.traverse_cache(test_cache, domains)

        self.assertEqual(a_record, '22.22.22.22')
        self.assertEqual(traversed_domains, ['.', 'com', 'google'])
        self.assertEqual(ns, '4.4.4.4')

    def test_fetching_a_nonexistent_a_record_at_lowest_level(self):
        """Desired outcome:
        No A record,
        all but one domain in traversed (we tried),
        ns at level above target (that's where we'll get new records)"""
        domains = [".", "com", "recurse"]

        a_record, traversed_domains, ns = scratchpad.traverse_cache(test_cache, domains)

        self.assertEqual(a_record, None)
        self.assertEqual(traversed_domains, ['.', 'com'])
        self.assertEqual(ns, '4.4.4.4')


class TestRecursiveDomain(unittest.TestCase):

    def test_looking_up_a_record_already_in_cache(self):
        domains = ['.', 'com', 'google']
        fqdn, a_record = scratchpad.recursively_look_up_domains(test_cache, domains)
        # self.assertEqual(fqdn, 'google.com')
        self.assertEqual(a_record, '22.22.22.22')

    def test_looking_up_record_not_in_cache_if_there_is_a_nameserver_at_higher_level(self):
        domains = ['.', 'com', 'recurse']
        fqdn, a_record = scratchpad.recursively_look_up_domains(test_cache, domains)
        self.assertEqual(a_record, '33.33.33.33')
        self.assertIsNotNone(test_cache['.']['subdomains']['com']['subdomains'].get('recurse'))

    def test_looking_up_record_not_in_cache_if_no_nameserver_at_immediately_higher_level(self):
        """I think expected behavior here is to start asking nameservers for other nameservers,
        which will need more sophisticated mocking"""
        domains = ['.', 'com', 'recurse', 'blog']
        assert False
