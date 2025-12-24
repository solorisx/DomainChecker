# Domain Checker

A Python tool to check domain name availability across multiple TLDs (.com, .ch, .org) by querying WHOIS servers directly.

## Features

- Check multiple domain names in one run
- Query multiple TLDs (.com, .ch, .org) for each domain
- Direct WHOIS server queries via socket connections (no external dependencies)
- Clean table-formatted summary output
- Real-time progress display

## Requirements

- Python 3.6+
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Create a `domains.txt` file with your domain names (one per line)

## Usage

1. Create a `domains.txt` file in the same directory with domain names to check:

```
mycompany
coolsite
awesomeapp
```

2. Run the script:

```bash
python domain_checker.py
```

3. View the results in a formatted table showing availability for each TLD.

## Output Example

```
======================================================================
SUMMARY TABLE
======================================================================
Domain Name          | .com       | .ch        | .org
----------------------------------------------------------------------
mycompany            | ✓ AVAIL    | ✗ TAKEN    | ✓ AVAIL
coolsite             | ✗ TAKEN    | ✓ AVAIL    | ✗ TAKEN
awesomeapp           | ✓ AVAIL    | ✓ AVAIL    | ✓ AVAIL
======================================================================

Legend: ✓ = Available  |  ✗ = Taken  |  ? = Error
```

## How It Works

The script connects directly to WHOIS servers on port 43 and queries domain information:
- Uses socket connections to query WHOIS servers
- Parses responses to determine domain availability
- Supports multiple TLDs with appropriate WHOIS server mapping

## Supported TLDs

Currently configured for:
- .com (whois.verisign-grs.com)
- .ch (whois.nic.ch)
- .org (whois.pir.org)

Additional TLDs can be added by extending the `whois_servers` dictionary in `get_whois_server()`.

## Limitations

- WHOIS queries may be rate-limited by some registrars
- Some TLDs may have different response formats
- Network connectivity required for all queries

## License

Free to use and modify.
