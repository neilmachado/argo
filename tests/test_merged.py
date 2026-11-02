import importlib.util
from io import StringIO
from unittest.mock import patch
import pytest
from rich.console import Console
from argus import passive
from argus.cli.main import modules,Menu
from argus.nonintrusive import lookup

@pytest.mark.parametrize('name',['server_info','asn_lookup','txt_records','dns_caa_checker','spf_dkim_dmarc_validator','http_headers','clickjacking_test','autocomplete_vulnerability_checker','third_party_integrations'])
def test_merged_entrypoints_removed(name):
    assert importlib.util.find_spec('argus.modules.'+name) is None


def test_ip_asn_is_one_provider_call_with_full_information():
    data={'ip':'8.8.8.8','country':'United States','connection':{'asn':15169,'org':'Google'}}
    with patch.object(passive,'get_json',return_value=data) as request:
        result=lookup('ip_info.py','8.8.8.8')
    assert result==data
    request.assert_called_once_with('https://ipwho.is/8.8.8.8')


def test_merged_dns_reuses_txt_and_has_caa_spf_dmarc():
    class Answer:
        def __init__(self,text):self.text=text
        def to_text(self):return self.text
    def resolve(name,kind,**kwargs):
        if name=='_dmarc.example.com':return [Answer('"v=DMARC1; p=reject"')]
        if kind=='TXT':return [Answer('"v=spf1 -all"')]
        if kind=='CAA':return [Answer('0 issue "example-ca.test"')]
        return []
    with patch('dns.resolver.Resolver.resolve',side_effect=resolve) as query:
        result=passive.lookup('dns_records.py','example.com')
    assert len(query.call_args_list)==9
    assert len([c for c in query.call_args_list if c.args==('example.com','TXT')])==1
    assert result['CAA'] and result['SPF'] and result['DMARC']


def test_sources_displayed_at_selection_and_execution_without_key_values():
    m=next(m for m in modules() if m['script']=='censys.py')
    out=StringIO();cli=Menu(Console(file=out,width=120),lambda _:m['id'])
    with patch('argus.cli.main.API_KEYS',{'CENSYS_PAT':'DO_NOT_PRINT'}),patch('argus.cli.main.record_lookup',return_value={}):
        cli.select_module();cli.run_module('8.8.8.8')
    text=out.getvalue()
    assert text.count('API: Censys Platform API')==2
    assert 'Host Records' in text and 'api.platform.censys.io' in text
    assert 'DO_NOT_PRINT' not in text


def test_every_retained_module_identifies_its_source():
    for m in modules():
        assert m['source'].startswith(('API:','Source:')) and m['source_details']
    offline=next(m for m in modules() if m['input_type']=='jwt')
    assert 'Offline' in offline['source']


def test_merged_http_uses_one_response_for_all_header_views():
    with patch('argus.nonintrusive.fetch_page',return_value={'status':200,'headers':{'Server':'Test','X-Frame-Options':'DENY'},'body':''}) as get:
        result=lookup('http_security.py','example.com')
    get.assert_called_once()
    assert result['headers']['Server']=='Test'
    assert result['security_headers']['X-Frame-Options']=='DENY'
    assert result['framing']['X-Frame-Options']=='DENY'


def test_merged_technology_uses_one_response_for_all_findings():
    with patch('argus.nonintrusive.fetch_page',return_value={'status':200,'headers':{'Server':'Test'},'body':'<meta name="generator" content="ExampleCMS"><script src="https://cdn.example.net/app.js"></script>'}) as get:
        result=lookup('technology_stack.py','example.com')
    get.assert_called_once()
    assert result['server']=='Test' and result['generators']==['ExampleCMS']
    assert result['referenced_hosts']==['cdn.example.net']
