"""Bounded DNS, public-record, offline and single-page inspection modules."""
import base64
import ipaddress
import json
import sys
import xml.etree.ElementTree as ET
from http.cookies import SimpleCookie
from urllib.parse import urlsplit, quote, urljoin
import dns.resolver
import requests
from bs4 import BeautifulSoup, Comment
from rich.console import Console

DNS = {'dns_over_https.py'}
RECORDS = {'archive_history.py','ip_info.py'}
WEB = {'pixel_tracker_finder.py', 'technology_stack.py', 'sitemap.py', 'form_grabber.py', 'crawl_rules.py', 'cookies.py', 'http_security.py', 'social_media.py', 'embedded_object_hunter.py', 'security_txt.py', 'html_comments_extractor.py', 'captcha_presence_checker.py'}
OFFLINE = {'jwt_token_analyzer.py'}
RESTORED = frozenset(DNS | RECORDS | WEB | OFFLINE)
console = Console()
PATHS = {'security_txt.py':'/.well-known/security.txt','crawl_rules.py':'/robots.txt','sitemap.py':'/sitemap.xml'}
SECURITY_HEADERS = ('Strict-Transport-Security','Content-Security-Policy','X-Frame-Options','X-Content-Type-Options','Referrer-Policy','Permissions-Policy')

def website_url(target, path='/'):
    from argus.passive import domain
    if path not in {'/','/.well-known/security.txt','/robots.txt','/sitemap.xml'}:
        raise ValueError('Only the homepage and standard metadata paths are allowed')
    parsed = urlsplit(target if '://' in target else 'https://'+target)
    if parsed.scheme not in ('http','https') or parsed.username or parsed.password or parsed.port not in (None, 443 if parsed.scheme == 'https' else 80) or parsed.query or parsed.fragment or parsed.path not in ('','/'):
        raise ValueError('Enter a bare domain or HTTP(S) origin; custom paths, ports and queries are disabled')
    host = parsed.hostname or ''
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        host = domain(host)
    else:
        if not ip.is_global: raise ValueError('A public hostname/IP is required')
        host = '['+str(ip)+']' if ip.version==6 else str(ip)
    return parsed.scheme+'://'+host+path

def fetch_page(target, path='/'):
    from argus.passive import MAX_BYTES
    url = website_url(target, path)
    with requests.Session() as session:
        session.trust_env = False
        with session.get(url, timeout=(5,15), verify=True, allow_redirects=False,stream=True,
                         headers={'User-Agent':'Arugus-by-Neil/2.2 (single-page inspection)'}) as response:
            # No fallback, retries, crawling, linked asset fetches, form submission or JS execution.
            if 300 <= response.status_code < 400:
                return {'status':response.status_code,'headers':dict(response.headers),'body':'','redirect_to':urljoin(url,response.headers.get('Location','')),'note':'Redirect not followed'}
            data=bytearray()
            for chunk in response.iter_content(65536):
                data.extend(chunk)
                if len(data)>MAX_BYTES:raise ValueError('Page exceeds response size limit')
            return {'status':response.status_code,'headers':dict(response.headers),'body':data.decode(response.encoding or 'utf-8',errors='replace')}

def dns_values(name, kind):
    resolver=dns.resolver.Resolver()
    try:return [r.to_text() for r in resolver.resolve(name,kind,lifetime=3,search=False)]
    except (dns.resolver.NXDOMAIN,dns.resolver.NoAnswer):return []
    except Exception:return ['Lookup failed or timed out']

def reference_host(value):
    try:
        return (urlsplit(value).hostname or '').lower()
    except ValueError:
        return ''

def inspect_page(script, page):
    headers=page['headers']; lower={k.lower():v for k,v in headers.items()}
    status = page['status']
    if 300 <= status < 400:
        destination = page.get('redirect_to') or lower.get('location', '')
        result = {'status': status, 'outcome': 'not_analyzed',
                  'note': 'The website redirected this request. Its final page was not fetched or analyzed; this is not an empty-findings result.',
                  'redirect_to': destination}
        # Suggest only a valid origin; never automatically fetch or follow it.
        if destination:
            try:
                parsed = urlsplit(destination)
                if parsed.path in ('', '/') and not parsed.query and not parsed.fragment:
                    origin = parsed.scheme + '://' + parsed.netloc
                    website_url(origin)
                    result['next_step'] = 'If you are permitted to check this destination, enter ' + origin + ' as the input.'
            except ValueError:
                pass
        return result
    if not 200 <= status < 300:
        return {'status': status, 'outcome': 'not_analyzed',
                'note': 'The requested page was not available (HTTP ' + str(status) + '). No page-content findings were produced.'}
    body=page['body']; soup=BeautifulSoup(body,'html.parser')
    result={'status':page['status']}
    if page.get('note'):result['note']=page['note']
    if script == 'http_security.py':
        result['headers'] = headers
        result['security_headers'] = {k:lower.get(k.lower(),'Not present') for k in SECURITY_HEADERS}
        result['framing'] = {k:lower.get(k.lower(),'Not present') for k in ('X-Frame-Options','Content-Security-Policy')}
        result['note'] = 'Raw headers, security headers and framing policy from one response. Observations do not prove a vulnerability.'
    elif script=='cookies.py':
        jar=SimpleCookie()
        try:jar.load(lower.get('set-cookie',''))
        except Exception:pass
        result['cookies']=[{'name':name,'secure':bool(c['secure']),'httponly':bool(c['httponly']),'samesite':c['samesite'],'path':c['path']} for name,c in jar.items()]
        result['note']='Homepage response only; combined cookie headers may omit details. Cookie values are not shown.'
    elif script in {'security_txt.py','crawl_rules.py'}:result['text']=body
    elif script=='sitemap.py':
        if '<!DOCTYPE' in body.upper() or '<!ENTITY' in body.upper():
            return {'status':status,'outcome':'not_analyzed','note':'Sitemap DTD/entity declarations are not accepted.'}
        try:
            xml = ET.fromstring(body)
            result['locations'] = [(n.text or '').strip() for n in xml.iter() if n.tag.rsplit('}',1)[-1] == 'loc'][:500]
        except ET.ParseError:
            return {'status':status,'outcome':'not_analyzed','note':'The response was not a valid XML sitemap.'}
        result['note']='Listed locations are not fetched; child sitemaps are not followed.'
    elif script=='html_comments_extractor.py':result['comments']=[str(n) for n in soup.find_all(string=lambda x:isinstance(x,Comment))][:100]
    elif script == 'form_grabber.py':
        result['forms']=[{'action':f.get('action',''),'method':f.get('method','GET'), 'autocomplete':f.get('autocomplete',''), 'fields':[{'name':i.get('name',''),'type':i.get('type','text'),'autocomplete':i.get('autocomplete','')} for i in f.find_all(['input','textarea','select'])][:100]} for f in soup.find_all('form')][:50]
        result['note']='Markup only; no forms submitted and no field values collected.'
    elif script=='captcha_presence_checker.py':result['indicators']=[x for x in ('recaptcha','hcaptcha','turnstile') if x in body.lower()]
    elif script=='social_media.py':result['links']=[a['href'] for a in soup.find_all('a',href=True) if reference_host(a['href']).removeprefix('www.') in {'facebook.com','instagram.com','linkedin.com','x.com','twitter.com','youtube.com','tiktok.com'}][:100]
    elif script=='embedded_object_hunter.py':result['embeds']=[{'tag':n.name,'source':n.get('src',n.get('data',''))} for n in soup.find_all(['iframe','object','embed'])][:100]
    elif script=='pixel_tracker_finder.py':result['possible_pixels']=[{'src':n.get('src',''),'width':n.get('width',''),'height':n.get('height','')} for n in soup.find_all('img') if n.get('width')=='1' or n.get('height')=='1'][:100]
    elif script == 'technology_stack.py':
        result.update(server=lower.get('server',''),powered_by=lower.get('x-powered-by',''),generators=[m.get('content','') for m in soup.find_all('meta',attrs={'name':'generator'})])
        result['referenced_hosts'] = sorted({reference_host(n.get('src',n.get('href',''))) for n in soup.find_all(['script','link','iframe']) if reference_host(n.get('src',n.get('href','')))})[:100]
        result['note'] = 'Technology hints and referenced integration hosts from one response; referenced hosts are not all necessarily third parties.'
    if script == 'social_media.py':
        result['note'] = 'Only social links present in this fetched HTML are listed. No search engines, linked pages or JavaScript were used.'
    return result

def lookup(script,target):
    from argus.passive import domain, get_json
    if script not in RESTORED:raise ValueError('Module is not reviewed')
    if script in WEB:return inspect_page(script,fetch_page(target,PATHS.get(script,'/')))
    if script in DNS:
        name=domain(target)
        return get_json('https://dns.google/resolve',params={'name':name,'type':'A'})
    if script=='archive_history.py':return get_json('https://web.archive.org/cdx/search/cdx',params={'url':domain(target)+'/*','output':'json','limit':50,'collapse':'urlkey'})
    if script == 'ip_info.py':
        ip=str(ipaddress.ip_address(target))
        result=get_json('https://ipwho.is/'+quote(ip,safe=''))
        return result
    if script=='jwt_token_analyzer.py':
        if len(target)>65536:raise ValueError('Token too large')
        parts=target.split('.')
        if len(parts)!=3:raise ValueError('Expected a three-part JWT')
        def decode(s):return json.loads(base64.urlsafe_b64decode(s+'='*(-len(s)%4)))
        return {'header':decode(parts[0]),'payload':decode(parts[1]),'note':'Decoded offline. Signature and claims NOT verified. Do not trust this token on this basis.'}

def main(script):
    try:
        if len(sys.argv)<2:raise ValueError('A target is required')
        console.print_json(data=lookup(script,sys.argv[1]))
    except Exception as exc:
        # No raw exception URLs or provider bodies: those may contain credentials.
        console.print('Lookup failed ('+type(exc).__name__+'). Check target format, TLS and provider access.',markup=False)
        raise SystemExit(1)
