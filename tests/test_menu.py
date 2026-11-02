from io import StringIO
from unittest.mock import patch
import pytest
from rich.console import Console
from argus.cli.main import Menu, modules, validate_input


def menu(answers):
    out=StringIO();answers=iter(answers)
    return Menu(Console(file=out,color_system=None,width=100),lambda _:next(answers)),out

def item(script):return next(m for m in modules() if m['script']==script)

def test_ids_are_sequential_and_inputs_are_documented():
    assert [int(m['id']) for m in modules()]==list(range(1,23))
    assert all(m['input_type'] and m['example'] for m in modules())

def test_menu_has_exactly_four_choices_and_exits():
    cli,out=menu(['4']);cli.run();text=out.getvalue()
    assert all(s in text for s in ['1. View modules','2. Select module','3. Run module','4. Exit'])
    assert 'Goodbye' in text and 'set target' not in text

def test_select_shows_input_example_and_does_not_run():
    m=item('dns_records.py');cli,out=menu([m['id']])
    with patch('argus.cli.main.restored_lookup',side_effect=AssertionError('No execution')):
        cli.select_module()
    assert 'Domain name' in out.getvalue() and 'example.com' in out.getvalue()

@pytest.mark.parametrize('script,value',[
 ('dns_records.py','8.8.8.8'),('dns_records.py','person@example.com'),
 ('dns_records.py','https://example.com'),('censys.py','example.com'),
 ('http_security.py','https://example.com/admin'),('jwt_token_analyzer.py','not-a-token')])
def test_invalid_input_does_not_run(script,value):
    cli,out=menu([value]);cli.selected=item(script)
    with patch('argus.cli.main.API_KEYS',{'CENSYS_PAT':'dummy'}),patch('argus.cli.main.record_lookup',side_effect=AssertionError('No network')),patch('argus.cli.main.restored_lookup',side_effect=AssertionError('No network')):
        cli.run_module()
    assert 'Invalid input' in out.getvalue()

def test_run_requires_selection():
    cli,out=menu([]);cli.run_module();assert 'Select a module before running' in out.getvalue()

def test_missing_key_blocks_run_without_requesting_input():
    cli,out=menu([]);cli.selected=item('censys.py')
    with patch('argus.cli.main.API_KEYS',{}):cli.run_module()
    assert 'Missing CENSYS_PAT' in out.getvalue()

def test_website_scheme_preserved_and_one_dispatch():
    cli,out=menu(['http://example.com']);cli.selected=item('http_security.py')
    with patch('argus.cli.main.restored_lookup',return_value={'status':200}) as run:
        cli.run_module()
    run.assert_called_once_with('http_security.py','http://example.com')
    assert 'Results were displayed only' in out.getvalue()

def test_blank_cancels_and_old_numbers_are_rejected():
    cli,out=menu(['118','']);cli.select_module();assert cli.selected is None
    cli.select_module();assert cli.selected is None


def test_ip_and_domain_inputs():
    assert validate_input(item('censys.py'),'2001:4860:4860::8888')=='2001:4860:4860::8888'
    assert validate_input(item('virustotal_scan.py'),'8.8.8.8')=='8.8.8.8'
    assert validate_input(item('virustotal_scan.py'),'Example.COM')=='example.com'

def test_full_guided_flow_with_mocked_dns():
    number=item('dns_records.py')['id'];cli,out=menu(['1',number,'','example.com','q'])
    with patch('argus.cli.main.record_lookup',return_value={'A':['192.0.2.1']}) as run:
        cli.run()
    run.assert_called_once_with('dns_records.py','example.com')
    assert '192.0.2.1' in out.getvalue()

def test_provider_error_does_not_leak_credentials():
    cli,out=menu(['example.com']);cli.selected=item('http_security.py')
    with patch('argus.cli.main.restored_lookup',side_effect=RuntimeError('SECRET TOKEN')):
        cli.run_module()
    assert 'SECRET TOKEN' not in out.getvalue() and 'Lookup failed' in out.getvalue()


def test_no_home_menu_repeated_after_selection_or_results():
    number=item('dns_records.py')['id']
    cli,out=menu(['2',number,'','example.com','','example.org','q'])
    with patch('argus.cli.main.record_lookup',return_value={'A':[]}) as run:
        cli.run()
    assert run.call_count==2
    assert out.getvalue().count('1. View modules')==1
    assert 'Choose 3' not in out.getvalue()

def test_only_explicit_home_navigation_redisplays_home_menu():
    number=item('dns_records.py')['id'];cli,out=menu(['2',number,'b','4'])
    cli.run()
    assert out.getvalue().count('1. View modules')==2

def test_invalid_selection_remains_in_selection_section():
    number=item('dns_records.py')['id'];cli,out=menu(['1','118',number,'q'])
    cli.run()
    assert out.getvalue().count('1. View modules')==1
    assert cli.selected['id']==number

def test_run_without_selection_guides_to_module_number():
    number=item('dns_records.py')['id'];cli,out=menu(['3',number,'q'])
    cli.run()
    assert 'Select a module before running.' in out.getvalue()
    assert cli.selected['id']==number


def test_ip_can_be_entered_directly_at_run_prompt():
    number=item('shodan.py')['id'];cli,out=menu(['2',number,'103.21.244.2','q'])
    with patch('argus.cli.main.API_KEYS',{'SHODAN_API_KEY':'dummy'}),patch('argus.cli.main.record_lookup',return_value={'ip':'103.21.244.2'}) as run:
        cli.run()
    run.assert_called_once_with('shodan.py','103.21.244.2')
    assert 'Finished.' in out.getvalue()


def test_direct_input_preserves_jwt_case():
    token=item('jwt_token_analyzer.py')['example'];number=item('jwt_token_analyzer.py')['id']
    cli,out=menu(['2',number,token,'q'])
    with patch('argus.cli.main.restored_lookup',return_value={}) as run:cli.run()
    run.assert_called_once_with('jwt_token_analyzer.py',token)


def test_shodan_membership_failure_explains_plan_restriction():
    from argus.passive import ProviderError
    cli,out=menu(['103.21.244.0']);cli.selected=item('shodan.py')
    with patch('argus.cli.main.API_KEYS',{'SHODAN_API_KEY':'dummy'}),patch('argus.cli.main.record_lookup',side_effect=ProviderError('api.shodan.io',403)):
        cli.run_module()
    assert 'HTTP 403' in out.getvalue() and 'membership' in out.getvalue()
    assert 'Lookup failed (ValueError)' not in out.getvalue()

@pytest.mark.parametrize('status,expected',[(401,'authentication'),(404,'no record'),(429,'rate limit')])
def test_provider_status_messages(status,expected):
    from argus.passive import ProviderError
    assert expected in str(ProviderError('api.shodan.io',status))
