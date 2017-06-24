## octoDNS DDNS

A simple Dynamic DNS source for octoDNS.

Supports both IPv4 and IPv6 addresses. Generally useful when you have a zone
with staticly configured records but would also like to include a dynamic
record, e.g. for your office or home on a non-fixed IP address.

By default it uses http://api.ident.me/ to find the public address of the
machine running the sync.

### Example config

The following config will combine the records in `./config/example.com.yaml`
and the dynamically looked up address at `dynamic.example.com.` creating both
IPv4 and IPv6 addresses.

```yaml
providers:

  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config

  dynamic:
    class: octodns_ddns.DdnsSource

  route53:
    class: octodns.provider.route53.Route53Provider
    access_key_id: env/AWS_ACCESS_KEY_ID
    secret_access_key: env/AWS_SECRET_ACCESS_KEY

zones:

  example.com.:
    sources:
      - config
      - dynamic  # will add dynamic.example.com.
    targets:
      - route53

```

You can configure it to only do `A` or `AAAA` by adding a `types` param to the
provider config.

```yaml
  dynamic:
    class: octodns_ddns.DdnsSource
    types:
      - A
```

### Configuring lookup urls

If you would like to use an alternate provider for looking up your address you
can configure `urls` with `a` and/or `aaaa` with urls that return the address
as the content of the response.

```yaml
  dynamic:
    class: octodns_ddns.DdnsSource
    urls:
      A: https://v4.ident.me/
      AAAA: https://v6.ident.me/
```
