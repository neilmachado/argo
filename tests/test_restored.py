from unittest.mock import patch
import base64,json
import pytest
from argo import nonintrusive as n

@pytest.mark.parametrize('target',['https://example.com/admin','https://example.com/?debug=1','https://user:pass@example.com','https://example.com:8443','file:///etc/passwd','127.0.0.1'])
def test_web_rejects_non_origin_inputs(target):
    with patch.object(n.requests,'Session',side_effect=AssertionError('Network must not start')):
        with pytest.raises(ValueError):n.fetch_page(target)

class Response:
    status_code=200
    headers={'Content-Type':'text/html'}
    encoding='utf-8'
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def iter_content(self,size):yield b'<a href="https://elsewhere.example/">link</a><form action="/delete" method="POST"><input name="password" value="secret"></form>'
class Session:
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def get(self,url,**kwargs):
        assert kwargs['verify'] and not kwargs['allow_redirects'] and kwargs['stream']
        assert not self.trust_env
        Session.urls.append(url)
        return Response()
    urls=[]

def test_homepage_inspection_one_get_no_form_submission_or_link_fetch():
    Session.urls=[]
    with patch.object(n.requests,'Session',Session):
        result=n.lookup('form_grabber.py','example.com')
    assert Session.urls==['https://example.com/']
    assert result['forms'][0]['method']=='POST'
    assert 'secret' not in json.dumps(result)

@pytest.mark.parametrize('script,path',list(n.PATHS.items()))
def test_only_one_standard_path(script,path):
    Session.urls=[]
    with patch.object(n.requests,'Session',Session):n.lookup(script,'example.com')
    assert Session.urls==['https://example.com'+path]

def test_redirect_is_reported_not_followed():
    Session.urls=[]
    with patch.object(n.requests,'Session',Session),patch.object(Response,'status_code',302):
        page=n.fetch_page('example.com')
    assert len(Session.urls)==1 and page['body']=='' and page['status']==302

def test_web_body_size_capped():
    from argo import passive
    with patch.object(n.requests,'Session',Session),patch.object(passive,'MAX_BYTES',1):
        with pytest.raises(ValueError,match='size limit'):n.fetch_page('example.com')

def test_dns_no_bruteforce_or_selector_guessing():
    from argo import passive
    with patch('dns.resolver.Resolver.resolve',return_value=[]) as query:
        passive.lookup('dns_records.py','example.com')
    assert len(query.call_args_list)==9
    assert [c.args for c in query.call_args_list][-1]==('_dmarc.example.com','TXT')
    assert all(c.args[1]!='AXFR' for c in query.call_args_list)

def test_jwt_is_offline_and_unverified():
    def part(v):return base64.urlsafe_b64encode(json.dumps(v).encode()).decode().rstrip('=')
    token=part({'alg':'none'})+'.'+part({'sub':'example'})+'.invalid'
    with patch.object(n.requests,'Session',side_effect=AssertionError('No network')):
        result=n.lookup('jwt_token_analyzer.py',token)
    assert result['payload']=={'sub':'example'} and 'NOT verified' in result['note']

def test_each_restored_module_has_bounded_dispatch():
    with patch.object(n,'fetch_page',return_value={'status':200,'headers':{},'body':''}) as fetch:
        for script in n.WEB:n.lookup(script,'example.com')
    assert fetch.call_count==len(n.WEB)
