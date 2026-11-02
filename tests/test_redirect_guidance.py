from io import StringIO
from unittest.mock import patch
import warnings
import pytest
from bs4 import XMLParsedAsHTMLWarning
from rich.console import Console
from argo.cli.main import Menu,modules,redirect_origin
from argo.nonintrusive import inspect_page


def test_only_same_site_www_https_is_offered():
    assert redirect_origin('https://google.com',{'status':301,'redirect_to':'https://www.google.com/'},'technology_stack.py')=='https://www.google.com'

@pytest.mark.parametrize('destination',[
 'https://other.example/','http://www.google.com/','https://www.google.com.evil.test/',
 'https://user:pass@www.google.com/','https://www.google.com:8443/',
 'https://www.google.com/path','https://www.google.com/?q=secret',
 'https://www.google.com/#fragment','https://google.com/'
])
def test_unsafe_or_different_redirects_are_not_offered(destination):
    assert redirect_origin('https://google.com',{'status':301,'redirect_to':destination},'technology_stack.py') is None


def test_no_request_to_redirect_without_user_action():
    module=next(m for m in modules() if m['script']=='technology_stack.py')
    answers=iter(['2',module['id'],'google.com','q']);out=StringIO()
    cli=Menu(Console(file=out,width=120),lambda _:next(answers))
    with patch('argo.cli.main.restored_lookup',return_value={'status':301,'outcome':'not_analyzed','redirect_to':'https://www.google.com/'}) as run:
        cli.run()
    run.assert_called_once_with('technology_stack.py','google.com')
    assert 'Type r below' in out.getvalue()


def test_explicit_r_makes_one_separate_same_site_request():
    module=next(m for m in modules() if m['script']=='technology_stack.py')
    answers=iter(['2',module['id'],'google.com','r','q']);out=StringIO()
    cli=Menu(Console(file=out,width=120),lambda _:next(answers))
    with patch('argo.cli.main.restored_lookup',side_effect=[{'status':301,'outcome':'not_analyzed','redirect_to':'https://www.google.com/'},{'status':200,'server':'gws'}]) as run:
        cli.run()
    assert [c.args[1] for c in run.call_args_list]==['google.com','https://www.google.com']
    assert cli.redirect_target is None


def test_denial_is_explained_and_offers_no_retry_destination():
    out=StringIO();cli=Menu(Console(file=out,width=120),lambda _: '')
    cli.selected=next(m for m in modules() if m['script']=='technology_stack.py')
    with patch('argo.cli.main.restored_lookup',return_value={'status':403,'outcome':'not_analyzed'}):cli.run_module('www.ebay.com')
    assert 'Access denied by the website' in out.getvalue() and cli.redirect_target is None


def test_sitemap_is_never_sent_to_html_parser():
    with warnings.catch_warnings():
        warnings.simplefilter('error',XMLParsedAsHTMLWarning)
        result=inspect_page('sitemap.py',{'status':200,'headers':{},'body':'<?xml version="1.0"?><urlset><url><loc>https://example.com/</loc></url></urlset>'})
    assert result['locations']==['https://example.com/']
