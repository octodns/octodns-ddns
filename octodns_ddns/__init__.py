'''
A simple Dynamic DNS source for octoDNS.

Supports both IPv4 and IPv6 addresses. Generally useful when you have a zone
with staticly configured records but would also like to include a dynamic
record, e.g. for your office or home on a non-fixed IP address.
'''

from requests import get
from logging import getLogger

from octodns.record import Record
from octodns.source.base import BaseSource

__VERSION__ = 0.2

class DdnsSource(BaseSource):

    SUPPORTS = ('A', 'AAAA')
    SUPPORTS_GEO = False

    def __init__(self, id, types=('A', 'AAAA'), urls={}, ttl=60):
        self.log = getLogger('DdnsSource[{}]'.format(id))

        super(DdnsSource, self).__init__(id)

        self.types = types
        self.ttl   = ttl

        self.urls = {
            'A': urls.get('A', 'https://v4.ident.me/'),
            'AAAA': urls.get('AAAA', 'https://v6.ident.me/')
        }

    def populate(self, zone, target=False):

        for _type in self.types:
            addr = get(self.urls[_type]).text

            if addr:
                record = Record.new(zone, self.id, {
                    'ttl': self.ttl,
                    'type': _type,
                    'value': addr
                }, source=self)

                zone.add_record(record)