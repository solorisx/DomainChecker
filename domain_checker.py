import socket

def check_domain_availability(domain_name):
    """
    Check if a domain name is available for registration.

    Args:
        domain_name (str): The domain name to check.
    Returns:
        bool: True if the domain is available, False if it is taken.
    """
    try:
        whois_server = get_whois_server(domain_name)
        whois_data = query_whois_server(whois_server, domain_name)

        # Check if the response indicates the domain is registered
        # Common indicators that a domain is taken
        taken_indicators = [
            'domain name:',
            'domain status:',
            'registrar:',
            'creation date:',
            'updated date:'
        ]

        whois_lower = whois_data.lower()
        for indicator in taken_indicators:
            if indicator in whois_lower:
                return False

        if 'no match' in whois_lower or 'not found' in whois_lower:
            return True

        return True

    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def get_whois_server(domain_name):
    """Get the appropriate WHOIS server for the domain."""
    tld = domain_name.split('.')[-1]

    # Common WHOIS servers
    whois_servers = {
        'com': 'whois.verisign-grs.com',
        'net': 'whois.verisign-grs.com',
        'org': 'whois.pir.org',
        'ch': 'whois.nic.ch',
        'info': 'whois.afilias.net',
        'biz': 'whois.biz',
        'us': 'whois.nic.us',
        'uk': 'whois.nic.uk',
        'co': 'whois.nic.co',
        'io': 'whois.nic.io',
        'de': 'whois.denic.de',
    }

    return whois_servers.get(tld, 'whois.internic.net')

def query_whois_server(server, domain):
    """Query a WHOIS server for domain information."""
    port = 43
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    try:
        sock.connect((server, port))
        sock.send(f"{domain}\r\n".encode())

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

        return response.decode('utf-8', errors='ignore')
    finally:
        sock.close()

def main():
    try:
        with open('domains.txt', 'r') as f:
            base_names = [line.strip() for line in f if line.strip()]

        # TLDs to check
        tlds = ['.com', '.ch', '.org']

        print(f"Checking {len(base_names)} name(s) across {len(tlds)} TLDs...\n")

        # Store results per domain name
        results = {}

        for base_name in base_names:
            # Remove any existing TLD from the base name
            if '.' in base_name:
                base_name = base_name.split('.')[0]

            print(f"\n{'='*50}")
            print(f"Checking '{base_name}' across all TLDs:")
            print(f"{'='*50}")

            results[base_name] = {}

            for tld in tlds:
                domain = base_name + tld
                print(f"\nChecking {domain}...")
                is_available = check_domain_availability(domain)

                # Store result
                tld_key = tld.replace('.', '')
                results[base_name][tld_key] = is_available

                if is_available is True:
                    print(f"  ✓ '{domain}' is AVAILABLE")
                elif is_available is False:
                    print(f"  ✗ '{domain}' is TAKEN")
                else:
                    print(f"  ? '{domain}' - Error occurred")

        # Summary Table
        print(f"\n\n{'='*70}")
        print("SUMMARY TABLE")
        print(f"{'='*70}")

        # Table header
        header = f"{'Domain Name':<20} | {'.com':<10} | {'.ch':<10} | {'.org':<10}"
        print(header)
        print("-" * 70)

        for base_name in base_names:
            if '.' in base_name:
                base_name = base_name.split('.')[0]

            com_status = format_status(results[base_name].get('com'))
            ch_status = format_status(results[base_name].get('ch'))
            org_status = format_status(results[base_name].get('org'))

            row = f"{base_name:<20} | {com_status:<10} | {ch_status:<10} | {org_status:<10}"
            print(row)

        print("=" * 70)
        print("\nLegend: ✓ = Available  |  ✗ = Taken  |  ? = Error")

    except FileNotFoundError:
        print("Error: domains.txt file not found.")
        print("Please create a domains.txt file with one domain name per line.")
        print("Example content:")
        print("  mycompany")
        print("  coolsite")
        print("  awesomeapp")

def format_status(status):
    """Format the status for table display."""
    if status is True:
        return "✓ AVAIL"
    elif status is False:
        return "✗ TAKEN"
    else:
        return "? ERROR"

if __name__ == "__main__":
    main()
