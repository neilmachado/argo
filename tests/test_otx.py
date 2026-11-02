from unittest.mock import patch
from io import StringIO
from rich.console import Console
import pytest
from argus import passive
from argus.cli.main import Menu,modules,validate_input

@pytest.mark.parametrize('value,kind,normalized',[
 ('8.8.8.8','IPv4','8.8.8.8'),('2001:4860:4860::8888','IPv6','2001:4860:4860::8888'),
 ('EXAMPLE.COM','domain','example.com'),('A'*32,'file','a'*32),('B'*40,'file','b'*40),('C'*64,'file','c'*64)])
def test_supported_indicators(value,kind,normalized):
    assert passive.otx_indicator(value)==(kind,normalized)

@pytest.mark.parametrize('value',['person@example.com','https://example.com/test','/tmp/file.exe','8.8.8.0/24','a'*31,'z'*64,'bad hash'])
def test_invalid_indicator_never_makes_a_request(value):
    with patch.object(passive,'get_json',side_effect=AssertionError('No request')):
        with pytest.raises(ValueError):passive.lookup('alienvault_otx.py',value)

@pytest.mark.parametrize('value,path',[('8.8.8.8','IPv4/8.8.8.8'),('example.com','domain/example.com'),('a'*64,'file/'+'a'*64),('2001:4860::8888','IPv6/2001%3A4860%3A%3A8888')])
def test_fixed_provider_get_and_only_otx_key(value,path):
    with patch.object(passive,'API_KEYS',{'OTX_API_KEY':'dummy-otx','SHODAN_API_KEY':'do-not-send'}),patch.object(passive,'get_json',return_value={'pulse_info':{'count':0}}) as get:
        result=passive.lookup('alienvault_otx.py',value)
    get.assert_called_once_with('https://otx.alienvault.com/api/v1/indicators/'+path+'/general',headers={'X-OTX-API-KEY':'dummy-otx'})
    assert 'do-not-send' not in str(get.call_args)
    assert 'do not establish safety' in result['note']

def test_missing_key_blocks_request():
    with patch.object(passive,'API_KEYS',{}),patch.object(passive,'get_json',side_effect=AssertionError('No request')):
        with pytest.raises(ValueError,match='OTX_API_KEY'):passive.lookup('alienvault_otx.py','8.8.8.8')

def test_otx_menu_and_input_guidance():
    module=next(m for m in modules() if m['script']=='alienvault_otx.py')
    assert module['id']=='22' and module['api_key']=='OTX_API_KEY'
    assert validate_input(module,'A'*64)=='a'*64
    answers=iter(['2','22','q']);output=StringIO()
    Menu(Console(file=output,width=100),lambda _:next(answers)).run()
    text=output.getvalue()
    assert 'AlienVault OTX' in text and 'MD5/SHA-1/SHA-256' in text
