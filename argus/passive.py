"""Reviewed dispatch allowlist and fixed-provider record client. Website checks live in nonintrusive.py."""
import ipaddress
import re
import json
import sys
from urllib.parse import quote, urlsplit
import requests
import dns.resolver
from rich.console import Console
from argus.config.settings import API_KEYS

from argus.nonintrusive import RESTORED

ALLOWED_SCRIPTS = RESTORED | frozenset({'dns_records.py', 'censys.py', 'shodan.py', 'virustotal_scan.py', 'ct_log_query.py', 'alienvault_otx.py'})
PROVIDERS = frozenset({'api.platform.censys.io', 'api.shodan.io', 'www.virustotal.com', 'crt.sh', 'dns.google', 'web.archive.org', 'ipwho.is', 'otx.alienvault.com'})
MAX_BYTES = 2_000_000
console = Console()

class ProviderError(ValueError):
    """Credential-safe explanation based on provider and HTTP status."""
    def __init__(self, host, status):
        provider = {
            'api.shodan.io': 'Shodan',
            'otx.alienvault.com': 'AlienVault OTX',
            'api.platform.censys.io': 'Censys',
            'www.virustotal.com': 'VirusTotal',
            'crt.sh': 'Certificate transparency provider',
            'dns.google': 'Google DNS',
            'web.archive.org': 'Wayback Machine',
            'ipwho.is': 'IP information provider',
        }.get(host, 'Provider')
        reasons = {
            401: 'rejected authentication. Check or replace the configured API key.',
            403: 'denied this lookup. Your account may lack the required plan or permissions.',
            404: 'has no record for this input.',
            429: 'rate limit reached. Wait before trying again.',
        }
        reason = reasons.get(status, 'returned an error. Try again later.')
        if host == 'otx.alienvault.com' and status == 403:
            reason = 'rejected access. Check the OTX API key and account permissions.'
        if host == 'api.shodan.io' and status == 403:
            reason = 'denied this host lookup. It may require membership or a higher plan; a configured key does not grant access to every record.'
        if 300 <= status < 400:
            reason = 'returned a redirect, which this tool does not follow.'
        super().__init__(f'{provider}: {reason} (HTTP {status})')
        self.status = status

def get_json(url, *, headers=None, params=None):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname not in PROVIDERS or parsed.username or parsed.port not in (None, 443):
        raise ValueError('Provider destination is not allowed')
    # Fixed GET-only client. Redirects, automatic retries and ambient proxies disabled.
    with requests.Session() as session:
        session.trust_env = False
        with session.get(url, headers=headers, params=params, timeout=(5, 20),
                         allow_redirects=False, verify=True, stream=True) as response:
            if response.status_code != 200:
                raise ProviderError(parsed.hostname, response.status_code)
            payload = bytearray()
            for chunk in response.iter_content(65536):
                payload.extend(chunk)
                if len(payload) > MAX_BYTES:
                    raise ValueError('Provider response exceeds size limit')
            return json.loads(payload)

def domain(value):
    value = value.strip().rstrip('.').encode('idna').decode('ascii')
    try:
        ipaddress.ip_address(value)
    except ValueError:
        pass
    else:
        raise ValueError('This module needs a domain name, not an IP address')
    if len(value)>253 or len(value.split('.'))<2 or any(not label or len(label)>63 or label.startswith('-') or label.endswith('-') or not all(c.isalnum() or c=='-' for c in label) for label in value.split('.')):
        raise ValueError('Enter a domain name without a URL or path')
    return value.lower()

def key(name):
    value = API_KEYS.get(name)
    if not value:
        raise ValueError(f'{name} is not configured')
    return value

def otx_indicator(value):
    """Infer supported indicator type without fetching/resolving the indicator."""
    value = value.strip()
    try:
        ip = ipaddress.ip_address(value)
        return ('IPv4' if ip.version == 4 else 'IPv6'), str(ip)
    except ValueError:
        pass
    if re.fullmatch(r'[a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}', value):
        return 'file', value.lower()
    try:
        return 'domain', domain(value)
    except ValueError:
        raise ValueError('Enter an IPv4/IPv6 address, a bare domain, or a 32/40/64-character hexadecimal MD5/SHA-1/SHA-256 hash. URLs, emails and files are not supported.') from None

def lookup(script, target):
    if script not in ALLOWED_SCRIPTS:
        raise ValueError('Module is not in the reviewed allowlist')
    if script == 'alienvault_otx.py':
        kind, value = otx_indicator(target)
        data = get_json(
            'https://otx.alienvault.com/api/v1/indicators/'+kind+'/'+quote(value,safe='')+'/general',
            headers={'X-OTX-API-KEY':key('OTX_API_KEY')},
        )
        return {'indicator':value,'indicator_type':kind,'note':'Existing OTX intelligence only. Pulse associations are not a conclusive maliciousness verdict; no matches do not establish safety.','data':data}
    if script == 'dns_records.py':
        name = domain(target)
        resolver = dns.resolver.Resolver()
        records = {}
        for kind in ('A','AAAA','MX','NS','TXT','CNAME','SOA'):
            try:
                records[kind] = [r.to_text() for r in resolver.resolve(name,kind,lifetime=3,search=False)]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                records[kind] = []
            except Exception:
                records[kind] = ['Lookup failed or timed out']
        return records
    if script == 'censys.py':
        ip = str(ipaddress.ip_address(target))
        return get_json('https://api.platform.censys.io/v3/global/asset/host/'+quote(ip,safe=''), headers={'Authorization':'Bearer '+key('CENSYS_PAT')})
    if script == 'shodan.py':
        ip = str(ipaddress.ip_address(target))
        return get_json('https://api.shodan.io/shodan/host/'+quote(ip,safe=''), params={'key':key('SHODAN_API_KEY')})
    if script == 'virustotal_scan.py':
        try:
            item = str(ipaddress.ip_address(target)); kind = 'ip_addresses'
        except ValueError:
            item = domain(target); kind = 'domains'
        return get_json('https://www.virustotal.com/api/v3/'+kind+'/'+quote(item,safe=''), headers={'x-apikey':key('VIRUSTOTAL_API_KEY')})
    return get_json('https://crt.sh/', params={'q':'%.'+domain(target),'output':'json'})

def main(script):
    if len(sys.argv)<2:
        console.print('A target is required.',markup=False); raise SystemExit(2)
    try:
        result = lookup(script,sys.argv[1])
        console.print_json(data=result)
    except Exception as exc:
        # Never print URLs, response bodies or exception details containing credentials.
        message = str(exc) if isinstance(exc, ValueError) and not isinstance(exc, requests.exceptions.RequestException) else type(exc).__name__
        console.print('Lookup failed: '+message,markup=False)
        raise SystemExit(1)
