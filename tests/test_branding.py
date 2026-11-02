from io import StringIO
from pathlib import Path
from unittest.mock import patch
from rich.console import Console
from threathawk.cli import logo


def test_text_branding_and_disclaimer():
    stream=StringIO();console=Console(file=stream,color_system=None,width=100)
    with patch.object(logo,'console',console):logo.logo('2.6.1',22,'neil')
    text=stream.getvalue()
    assert 'THREATHAWK' in text and 'LEGAL DISCLAIMER' in text and 'Coded by: neil' in text
    assert 'TERMINAL ONLY' not in text


def test_portrait_is_not_required_for_startup():
    assert not hasattr(logo,'portrait')
    assert not (Path(logo.__file__).resolve().parents[1]/'data/logo.json').exists()


def test_public_source_has_no_portrait_reference():
    source=Path(logo.__file__).read_text()
    assert 'neil-logo.png' not in source and 'logo.json' not in source
