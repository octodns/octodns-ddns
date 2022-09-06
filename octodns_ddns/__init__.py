'''
A simple Dynamic DNS source for octoDNS.

Supports both IPv4 and IPv6 addresses. Generally useful when you have a zone
with staticly configured records but would also like to include a dynamic
record, e.g. for your office or home on a non-fixed IP address.
'''

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from dns import tsigkeyring
from dns.update import Update as DnsUpdate
from dns.query import tcp as dns_query_tcp
from requests import Session
from requests.exceptions import ConnectionError
from logging import getLogger

from octodns.record import Create, Delete, Record, Update
from octodns.source.base import BaseSource
from octodns.provider.base import BaseProvider

__VERSION__ = '0.2.1'


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
            'AAAA': urls.get('AAAA', 'https://v6.ident.me/'),
        }

        self._sess = Session()

    def _get_addr(self, _type):
        self.log.debug('_get_addr: type=%s', _type)
        try:
            resp = self._sess.get(self.urls[_type])
        except ConnectionError:
            raise Exception(
                'Failed to get ip address for type={}'.format(_type)
            )
        resp.raise_for_status()
        addr = resp.content.decode('utf-8')
        self.log.info('_get_addr: type=%s is %s', _type, addr)
        return addr

    def populate(self, zone, target=False):
        self.log.debug('populate: zone=%s', zone.name)
        before = len(zone.records)

        for _type in self.types:
            addr = self._get_addr(_type)
            if addr:
                record = Record.new(
                    zone,
                    self.id,
                    {'ttl': self.ttl, 'type': _type, 'value': addr},
                    source=self,
                )
                zone.add_record(record)

        self.log.info(
            'populate:   found %s records', len(zone.records) - before
        )


class Rfc2136Provider(BaseProvider):
    SUPPORTS_GEO = False
    SUPPORTS_DYNAMIC = False
    # TODO: what else is supported/does it depend on the server?
    SUPPORTS = set(('A', 'AAAA'))

    def __init__(self, id, host, port, key_name, key_secret, *args, **kwargs):
        self.log = getLogger(f'Rfc2136Provider[{id}]')
        self.log.debug(
            '__init__: id=%s, host=%s, port=%s, key_name=%s, key_secret=***',
            id,
            host,
            port,
            key_name,
        )
        super().__init__(id, *args, **kwargs)
        self.host = host
        self.port = port
        self.key_name = key_name
        self.key_secret = key_secret

    def populate(self, zone, target=False, lenient=False):
        self.log.debug(
            'populate: name=%s, target=%s, lenient=%s',
            zone.name,
            target,
            lenient,
        )

        before = len(zone.records)

        # TODO: AXFR?

        self.log.info(
            'populate:   found %s records', len(zone.records) - before
        )
        # RFC-2136 7.6: States it's not possible to create zones, so we'll
        # assume it exists and let things blow up during apply if there are
        # problems
        return True

    def _apply(self, plan):
        # Store the zone with its records
        desired = plan.desired
        name = desired.name

        keyring = tsigkeyring.from_text({self.key_name: self.key_secret})
        batch = DnsUpdate(name, keyring=keyring)

        for change in plan.changes:
            if isinstance(change, Create):
                new = change.new
                # TODO: multiple values
                batch.add(new.fqdn, new.ttl, new._type, *new.values)
            elif isinstance(change, Update):
                new = change.new
                # TODO: multiple values
                batch.update(new.fqdn, new.ttl, new._type, *new.values)
            elif isinstance(change, Delete):
                existing = change.existing
                batch.delete(
                    existing.fqdn, existing.ttl, existing._type, existing.values
                )

        # TODO: port?
        # TODO: error handling?
        dns_query_tcp(batch, self.host)

        self.log.debug(
            '_apply: zone=%s, num_records=%d', name, len(plan.changes)
        )

        return True
