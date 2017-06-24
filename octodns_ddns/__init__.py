'''
A simple Dynamic DNS source for octoDNS.

Supports both IPv4 and IPv6 addresses. Generally useful when you have a zone
with staticly configured records but would also like to include a dynamic
record, e.g. for your office or home on a non-fixed IP address.
'''

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from requests import Session
from requests.exceptions import ConnectionError
from logging import getLogger

from octodns.record import Record
from octodns.source.base import BaseSource

__VERSION__ = 0.1


class DdnsSource(BaseSource):
    SUPPORTS_GEO = False
    SUPPORTS = ('A', 'AAAA')

    def __init__(self, id, types=('A', 'AAAA'), urls={}, ttl=60):
        self.log = getLogger('DdnsSource[{}]'.format(id))
        self.log.debug('__init__: id=%s, types=%s, ttl=%d', id, types, ttl)
        super(DdnsSource, self).__init__(id)
        self.types = types
        self.ttl = ttl
        self.urls = {
            'A': urls.get('A', 'https://v4.ident.me/'),
            'AAAA': urls.get('AAAA', 'https://v6.ident.me/')
        }

        self._sess = Session()

    def _get_addr(self, _type):
        self.log.debug('_get_addr: type=%s', _type)
        try:
            resp = self._sess.get(self.urls[_type])
        except ConnectionError:
            raise Exception('Failed to get ip address for type={}'
                            .format(_type))
        resp.raise_for_status()
        addr = resp.content
        self.log.info('_get_addr: type=%s is %s', _type, addr)
        return addr

    def populate(self, zone, target=False):
        self.log.debug('populate: zone=%s', zone.name)
        before = len(zone.records)

        for _type in self.types:
            addr = self._get_addr(_type)
            if addr:
                record = Record.new(zone, self.id, {
                    'ttl': self.ttl,
                    'type': _type,
                    'value': addr
                }, source=self)
                zone.add_record(record)

        self.log.info('populate:   found %s records',
                      len(zone.records) - before)
