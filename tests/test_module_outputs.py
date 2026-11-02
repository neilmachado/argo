from unittest.mock import patch
from io import StringIO
import pytest
from rich.console import Console
from threathawk.nonintrusive import inspect_page,WEB,lookup
from threathawk.cli.main import modules,Menu
from threathawk import passive

HTML='''<!doctype html><html><head><meta name="generator" content="ExampleCMS"><script src="https://cdn.example.net/app.js"></script></head><body><!--audit comment--><a href="https://www.linkedin.com/company/example">Social</a><form method="POST" action="/submit"><input type="email" name="email" autocomplete="off" value="PRIVATE"></form><div class="h-captcha">hcaptcha</div><iframe src="https://video.example.net/embed"></iframe><img src="/pixel.gif" width="1" height="1"></body></html>'''
PAGE={'status':200,'headers':{'Server':'ExampleServer','Content-Type':'text/html','X-Frame-Options':'DENY','Set-Cookie':'sid=PRIVATE; Secure; HttpOnly; SameSite=Lax'},'body':HTML}

@pytest.mark.parametrize('script,key,expected',[
 ('http_security.py','headers','ExampleServer'),('cookies.py','cookies','sid'),
 ('http_security.py','headers','DENY'),('http_security.py','headers','DENY'),
 ('html_comments_extractor.py','comments','audit comment'),('form_grabber.py','forms','email'),
 ('form_grabber.py','forms','off'),('captcha_presence_checker.py','indicators','hcaptcha'),
 ('social_media.py','links','linkedin.com'),('embedded_object_hunter.py','embeds','video.example.net'),
 ('pixel_tracker_finder.py','possible_pixels','pixel.gif'),('technology_stack.py','generators','ExampleCMS'),
 ('technology_stack.py','referenced_hosts','cdn.example.net')])
def test_positive_static_html_findings(script,key,expected):
    result=inspect_page(script,PAGE)
    assert expected in str(result[key])
    assert 'PRIVATE' not in str(result.get('forms',result.get('cookies','')))

@pytest.mark.parametrize('script',sorted(WEB))
@pytest.mark.parametrize('status',[301,403,404,429,500])
def test_non_success_never_looks_like_empty_findings(script,status):
    result=inspect_page(script,{'status':status,'headers':{'Location':'https://www.example.com/'},'redirect_to':'https://www.example.com/','body':''})
    assert result['outcome']=='not_analyzed' and result['status']==status
    assert not any(k in result for k in ('links','forms','cookies','locations','indicators'))

def test_redirect_gives_destination_without_fetching_it():
    result=inspect_page('social_media.py',{'status':301,'headers':{},'body':'','redirect_to':'https://www.example.com/'})
    assert 'https://www.example.com' in result['next_step']

def test_namespaced_sitemap():
    xml='<s:urlset xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"><s:url><s:loc>https://example.com/page</s:loc></s:url></s:urlset>'
    result=inspect_page('sitemap.py',{'status':200,'headers':{},'body':xml})
    assert result['locations']==['https://example.com/page']

@pytest.mark.parametrize('body',['not XML','<!DOCTYPE urlset [<!ENTITY x "boom">]><urlset/>'])
def test_bad_sitemap_is_not_a_success(body):
    assert inspect_page('sitemap.py',{'status':200,'headers':{},'body':body})['outcome']=='not_analyzed'

@pytest.mark.parametrize('script', ['security_txt.py','crawl_rules.py'])
def test_standard_metadata_returns_content(script):
    assert inspect_page(script,{'status':200,'headers':{},'body':'Contact: mailto:security@example.com'})['text'].startswith('Contact:')

def test_menu_does_not_say_finished_for_redirect():
    output=StringIO();cli=Menu(Console(file=output,width=100),lambda _: '')
    cli.selected=next(m for m in modules() if m['script']=='social_media.py')
    with patch('threathawk.cli.main.restored_lookup',return_value={'status':301,'outcome':'not_analyzed','note':'Redirect'}):
        cli.run_module('example.com')
    assert 'Not analyzed.' in output.getvalue() and 'Finished.' not in output.getvalue()

@pytest.mark.parametrize('m',modules(),ids=lambda m:m['id']+'-'+m['script'])
def test_every_module_dispatches_with_controlled_responses(m):
    target='8.8.8.8' if m['input_type'] in ('ip','domain_or_ip','otx_indicator') else m['example'] if m['input_type']=='jwt' else 'example.com'
    def provider(url,**kwargs):
        if 'ipwho.is' in url:return {'success':True,'connection':{'asn':15169}}
        if 'crt.sh' in url or 'web.archive.org' in url:return []
        return {'result':{},'pulse_info':{'count':0}}
    class Answer:
        def to_text(self):return '"v=spf1 -all"'
    page=PAGE if m['script'] not in ('sitemap.py',) else {'status':200,'headers':{},'body':'<urlset><url><loc>https://example.com/</loc></url></urlset>'}
    with patch('threathawk.nonintrusive.fetch_page',return_value=page),patch.object(passive,'get_json',side_effect=provider),patch.object(passive,'API_KEYS',{'CENSYS_PAT':'dummy','SHODAN_API_KEY':'dummy','VIRUSTOTAL_API_KEY':'dummy','OTX_API_KEY':'dummy'}),patch('dns.resolver.Resolver.resolve',return_value=[Answer()]):
        result=lookup(m['script'],target) if m['script'] in __import__('threathawk.nonintrusive',fromlist=['RESTORED']).RESTORED else passive.lookup(m['script'],target)
    assert result is not None


@pytest.mark.parametrize('script,key', [('social_media.py','links'),('technology_stack.py','referenced_hosts')])
def test_malformed_link_does_not_crash_page_analysis(script,key):
    page=dict(PAGE,body=HTML+'<a href="http://[invalid">bad</a><script src="http://[invalid"></script>')
    assert inspect_page(script,page)[key]

@pytest.mark.parametrize('origin',['https://example.com:80','http://example.com:443'])
def test_nondefault_scheme_ports_are_not_silently_rewritten(origin):
    from threathawk.nonintrusive import website_url
    with pytest.raises(ValueError):website_url(origin)
