## octoDNS DDNS

A simple Dynamic DNS source for [octoDNS](https://github.com/octodns/octodns/).

Supports both IPv4 and IPv6 addresses. Generally useful when you have a zone
with staticly configured records but would also like to include a dynamic
record, e.g. for your office or home on a non-fixed IP address.

By default it uses http://api.ident.me/ to find the public address of the
machine running the sync.



### Installation

#### Command line

```
pip install octodns-ddns
```

#### requirements.txt/setup.py

Pinning specific versions or SHAs is recommended to avoid unplanned upgrades.

##### Versions

```
# Start with the latest versions and don't just copy what's here
octodns==0.9.14
octodns-ddns==0.0.1
```

##### SHAs

```
# Start with the latest/specific versions and don't just copy what's here
-e git+https://git@github.com/octodns/octodns.git@9da19749e28f68407a1c246dfdf65663cdc1c422#egg=octodns
-e git+https://git@github.com/octodns/octodns-ddns.git@ec9661f8b335241ae4746eea467a8509205e6a30#egg={MODULE}
```

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
    # Defaults:
    A: https://api.idify.org/
    AAAA: https://api6.idify.org/
```

#### Alternatives

The following have been tested and confirmed to work as of the time they were added to this document.

| Service                                | IPv4 URL                      | IPv6 URL                      |
| :------------------------------------- | :---------------------------- | :---------------------------- |
| [ipify.org](https://www.ipify.org)     | `https://api.ipify.org`       | `https://api6.ipify.org`      |
| [icanhazip.com](https://icanhazip.com) | `https://ipv4.icanhazip.com`  | `https://ipv6.icanhazip.com`  |
| [ipinfo.io](https://ipinfo.io)         | `https://v4.api.ipinfo.io/ip` | `https://v6.api.ipinfo.io/ip` |
| [ident.me](https://ident.me)           | `https://v4.ident.me/`        | `https://v6.ident.me/`        |
