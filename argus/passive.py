"""Reviewed dispatch allowlist and fixed-provider record client. Website checks live in nonintrusive.py."""
import ipaddress
import json
import sys
from urllib.parse import quote, urlsplit
import requests
import dns.resolver
from rich.console import Console
from argus.config.settings import API_KEYS

from argus.nonintrusive import RESTORED

ALLOWED_SCRIPTS = RESTORED | frozenset({'dns_records.py', 'censys.py', 'shodan.py', 'virustotal_scan.py', 'ct_log_query.py'})
PROVIDERS = frozenset({'api.platform.censys.io', 'api.shodan.io', 'www.virustotal.com', 'crt.sh', 'dns.google', 'web.archive.org', 'ipwho.is'})
MAX_BYTES = 2_000_000
console = Console()

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
                raise ValueError(f'Provider returned HTTP {response.status_code}; no redirect or retry performed')
            payload = bytearray()
            for chunk in response.iter_content(65536):
                payload.extend(chunk)
                if len(payload) > MAX_BYTES:
                    raise ValueError('Provider response exceeds size limit')
            return json.loads(payload)

def domain(value):
    value = value.strip().rstrip('.').encode('idna').decode('ascii')
    if len(value)>253 or len(value.split('.'))<2 or any(not label or len(label)>63 or label.startswith('-') or label.endswith('-') or not all(c.isalnum() or c=='-' for c in label) for label in value.split('.')):
        raise ValueError('Enter a domain name without a URL or path')
    return value.lower()

def key(name):
    value = API_KEYS.get(name)
    if not value:
        raise ValueError(f'{name} is not configured')
    return value

def lookup(script, target):
    if script not in ALLOWED_SCRIPTS:
        raise ValueError('Module is not in the reviewed allowlist')
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
