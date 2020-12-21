import unittest

from mock import call, patch

from octodns.zone import Zone
from octodns_ddns import DdnsSource

class MockResponse(object):

    def __init__(self, content=None, raise_for_status=False):
        self.text = content

class TestDdnsSource(unittest.TestCase):

    @patch('requests.get')
    def test_defaults(self, mock):
        a_value = '1.2.3.4'
        aaaa_value = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        mock.side_effect = [
            MockResponse(a_value),
            MockResponse(aaaa_value)
        ]

        zone = Zone('example.com.', [])
        DdnsSource('dynamic').populate(zone)
        records = sorted(list(zone.records))
        self.assertEqual(2, len(records))
        a = records[0]
        self.assertEqual([a_value], a.values)
        aaaa = records[1]
        self.assertEqual([aaaa_value], aaaa.values)

        mock.assert_has_calls([
            call('https://v4.ident.me/'),
            call('https://v6.ident.me/')
        ])

    @patch('requests.get')
    def test_error(self, mock):
        mock.side_effect = [
            MockResponse(raise_for_status='boom'),
        ]
        zone = Zone('example.com.', [])

        with self.assertRaises(Exception):
            DdnsSource('dynamic').populate(zone)

    @patch('requests.get')
    def test_types_a(self, mock):
        a_value = '1.2.3.4'
        mock.side_effect = [
            MockResponse(a_value),
        ]

        zone = Zone('example.com.', [])
        DdnsSource('dynamic', types=('A',)).populate(zone)
        self.assertEqual(1, len(zone.records))

        mock.assert_has_calls([
            call('https://v4.ident.me/'),
        ])
        mock.assert_called_once()

    @patch('requests.get')
    def test_types_aaaa(self, mock):
        aaaa_value = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        mock.side_effect = [
            MockResponse(aaaa_value),
        ]

        zone = Zone('example.com.', [])
        DdnsSource('dynamic', types=('AAAA',)).populate(zone)
        self.assertEqual(1, len(zone.records))

        mock.assert_has_calls([
            call('https://v6.ident.me/'),
        ])
        mock.assert_called_once()

    @patch('requests.get')
    def test_urls(self, mock):
        a_value = '1.2.3.4'
        aaaa_value = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        mock.side_effect = [
            MockResponse(a_value),
            MockResponse(aaaa_value)
        ]

        zone = Zone('example.com.', [])
        DdnsSource('dynamic', urls={
            'A': 'https://foo.bar/v4',
            'AAAA': 'https://foo.bar/v6',
        }).populate(zone)
        records = sorted(list(zone.records))
        self.assertEqual(2, len(records))
        a = records[0]
        self.assertEqual([a_value], a.values)
        aaaa = records[1]
        self.assertEqual([aaaa_value], aaaa.values)

        mock.assert_has_calls([
            call('https://foo.bar/v4'),
            call('https://foo.bar/v6')
        ])

if __name__ == '__main__':
    unittest.main()