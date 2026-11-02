import importlib.util
import json
from pathlib import Path
from unittest.mock import patch
import pytest
from threathawk import passive
from threathawk.core import runner
from threathawk.cli.catalog.loader import load

@pytest.mark.parametrize('module',['open_ports','exposed_api_endpoints','rate_limit_waf_bypass_test','zonetransfer','performance_monitoring','snmp_public_community_checker','hidden_parameter_discovery'])
def test_removed_modules_unavailable(module):
    assert importlib.util.find_spec('threathawk.modules.'+module) is None

def test_catalog_and_physical_modules_exactly_match():
    catalog=load()
    assert {m['script'] for entries in catalog.values() for m in entries} == passive.ALLOWED_SCRIPTS
    import threathawk.modules
    assert {p.name for p in Path(threathawk.modules.__file__).parent.glob('*.py') if p.name!='__init__.py'}==passive.ALLOWED_SCRIPTS

def test_runner_blocks_paths_and_removed_modules():
    with patch.object(runner.subprocess,'Popen',side_effect=AssertionError('Unexpected execution')):
        for script in ['open_ports.py','../modules/open_ports.py','exposed_api_endpoints.py','/tmp/probe.py']:
            assert runner.execute_script(script,'example.com')==''

def test_external_catalog_ignored(monkeypatch,tmp_path):
    p=tmp_path/'modules.json';p.write_text('{"network_infrastructure":[{"script":"open_ports.py"}]}')
    monkeypatch.setenv('THREATHAWK_CATALOG_PATH',str(p))
    assert all(m['script'] in passive.ALLOWED_SCRIPTS for entries in load().values() for m in entries)

@pytest.mark.parametrize('url',['http://crt.sh/','https://example.com/','https://crt.sh.evil.test/','https://user@crt.sh/','https://crt.sh:8443/'])
def test_forbidden_destinations(url):
    with patch.object(passive.requests,'Session',side_effect=AssertionError('Network must not start')):
        with pytest.raises(ValueError):passive.get_json(url)

class Response:
    status_code=200
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def iter_content(self,size):yield b'{"ok":true}'
class Session:
    trust_env=True
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def get(self,url,**kwargs):
        assert kwargs['verify'] is True and kwargs['allow_redirects'] is False
        assert kwargs['stream'] is True and kwargs['timeout']==(5,20)
        assert self.trust_env is False
        return Response()

def test_client_verifies_tls_and_disables_redirects_proxies():
    with patch.object(passive.requests,'Session',Session):
        assert passive.get_json('https://crt.sh/')=={'ok':True}

def test_redirect_not_followed():
    with patch.object(passive.requests,'Session',Session),patch.object(Response,'status_code',302):
        with pytest.raises(ValueError,match='302'):passive.get_json('https://crt.sh/')

def test_response_size_limit():
    with patch.object(passive.requests,'Session',Session),patch.object(passive,'MAX_BYTES',2):
        with pytest.raises(ValueError,match='size limit'):passive.get_json('https://crt.sh/')

def test_provider_lookups_never_resolve_or_connect_to_target(monkeypatch):
    monkeypatch.setattr(passive,'API_KEYS',{'CENSYS_PAT':'dummy','SHODAN_API_KEY':'dummy','VIRUSTOTAL_API_KEY':'dummy'})
    calls=[]
    def fake(url,**kwargs): calls.append((url,kwargs));return {}
    with patch.object(passive,'get_json',fake):
        for script,target in [('censys.py','8.8.8.8'),('shodan.py','8.8.8.8'),('virustotal_scan.py','example.com'),('ct_log_query.py','example.com')]:
            passive.lookup(script,target)
    assert len(calls)==4
    assert all(passive.urlsplit(url).hostname in passive.PROVIDERS for url,_ in calls)
    assert '/api/v3/domains/example.com' in calls[2][0]
    with pytest.raises(ValueError):passive.lookup('censys.py','example.com')

def test_dns_fixed_types_and_no_axfr():
    with patch.object(passive.dns.resolver.Resolver,'resolve',return_value=[]) as query:
        passive.lookup('dns_records.py','example.com')
        assert [call.args[1] for call in query.call_args_list]==['A','AAAA','MX','NS','TXT','CNAME','SOA','CAA','TXT']
