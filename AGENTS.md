# Developer Agent Guide for octoDNS Dynamic DNS (DDNS) Source

This repository contains the Dynamic DNS (DDNS) source for octoDNS. It is a read-only source designed to discover the current public IPv4/IPv6 addresses of the executing environment (e.g. for home or office zones on dynamic IPs) and populate them as `A` or `AAAA` records.

> [!IMPORTANT]
> **Core Workflow and Guidelines**
>
> All agents working on this repository must read and follow the general instructions and workflow guidelines defined in the core octoDNS `AGENTS.md` file.
> - **Local check**: Look for the file at `../octodns/AGENTS.md`.
> - **Remote check**: If the local file is not available, fetch it from GitHub: [octoDNS Core AGENTS.md](https://github.com/octodns/octodns/raw/refs/heads/main/AGENTS.md).
>
> You must align your code structure, style, pull request guidelines, and overall development workflows with the instructions specified there.

## Repository & Module Information

### Key Components

- **Source Class**: [DnsSource](file:///home/ross/octodns/octodns-ddns/octodns_ddns/__init__.py#L29-L85) (defined in [octodns_ddns/__init__.py](file:///home/ross/octodns/octodns-ddns/octodns_ddns/__init__.py)). This is the core source making HTTP calls to fetch public IPs.

### Key Workflows & Features

1. **Supported Record Types**: `A`, `AAAA`.
2. **Public IP Discovery**: Resolves the current host's public IP address by querying remote endpoint APIs (which default to `https://api.ipify.org/` for IPv4 A records and `https://api6.ipify.org/` for IPv6 AAAA records). Allows overriding query URLs via the `urls` configuration dictionary.
3. **Record Configuration**: Populates dynamic IP records under a subdomain matching the source's `id` (e.g. `office.example.com.`) with a default TTL of `60` seconds.
4. **Dynamic Routing**: Not supported (`SUPPORTS_DYNAMIC=False`, `SUPPORTS_GEO=False`).
5. **Non-Provider nature**: `DnsSource` is a read-only source. It does not plan changes or write values. It must be paired with an active DNS target provider to apply the resolved IP records.

## Development & Testing

- **Setup Script**: Run `./script/bootstrap` to create a virtual environment, install dependencies (including `black`, `isort`, `pyflakes`, and `pytest`), and configure pre-commit hooks.
- **Test Suite**: Run unit tests using `pytest` via `./script/test` (or `pytest tests/`). Test files are located in [tests/](file:///home/ross/octodns/octodns-ddns/tests).
- **Code Coverage**: Verify code coverage using `./script/coverage`.

## Key Constraints & Behaviors

- **Python Version**: Targets Python `>=3.9`.
- **Formatting**: Code formatting is enforced via `black` (version `>=26.0.0,<27.0.0`) and `isort`.
