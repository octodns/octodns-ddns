#
#
#

from mock import call, patch
from octodns.zone import Zone
from unittest import TestCase

from octodns_ddns import DdnsSource


class MockResponse(object):

    def __init__(self, content=None, raise_for_status=False):
        self.content = content
        self._raise_for_status = raise_for_status

    def raise_for_status(self):
        if self._raise_for_status:
            raise Exception(self._raise_for_status)


class TestDdnsSource(TestCase):

    @patch('requests.Session.get')
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
        self.assertEquals(2, len(records))
        a = records[0]
        self.assertEquals([a_value], a.values)
        aaaa = records[1]
        self.assertEquals([aaaa_value], aaaa.values)

        mock.assert_has_calls([
            call('https://v4.ident.me/'),
            call('https://v6.ident.me/')
        ])

    @patch('requests.Session.get')
    def test_error(self, mock):
        mock.side_effect = [
            MockResponse(raise_for_status='boom'),
        ]
        zone = Zone('example.com.', [])

        with self.assertRaises(Exception):
            DdnsSource('dynamic').populate(zone)

    @patch('requests.Session.get')
    def test_types_a(self, mock):
        a_value = '1.2.3.4'
        mock.side_effect = [
            MockResponse(a_value),
        ]

        zone = Zone('example.com.', [])
        DdnsSource('dynamic', types=('A',)).populate(zone)
        self.assertEquals(1, len(zone.records))

        mock.assert_has_calls([
            call('https://v4.ident.me/'),
        ])
        mock.assert_called_once()

    @patch('requests.Session.get')
    def test_types_aaaa(self, mock):
        aaaa_value = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        mock.side_effect = [
            MockResponse(aaaa_value),
        ]

        zone = Zone('example.com.', [])
        DdnsSource('dynamic', types=('AAAA',)).populate(zone)
        self.assertEquals(1, len(zone.records))

        mock.assert_has_calls([
            call('https://v6.ident.me/'),
        ])
        mock.assert_called_once()

    @patch('requests.Session.get')
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
        self.assertEquals(2, len(records))
        a = records[0]
        self.assertEquals([a_value], a.values)
        aaaa = records[1]
        self.assertEquals([aaaa_value], aaaa.values)

        mock.assert_has_calls([
            call('https://foo.bar/v4'),
            call('https://foo.bar/v6')
        ])
