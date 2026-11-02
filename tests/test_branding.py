from io import StringIO
from unittest.mock import patch
import json
from pathlib import Path
from rich.console import Console
from threathawk.cli import logo


def test_supplied_portrait_data_is_packaged_and_square():
    pixels=json.loads((Path(logo.__file__).resolve().parents[1]/'data/logo.json').read_text())
    assert len(pixels)==32 and all(len(row)==32 for row in pixels)
    assert all(len(rgb)==3 and all(0<=c<=255 for c in rgb) for row in pixels for rgb in row)


def test_new_brand_and_disclaimer_with_plain_terminal_fallback():
    stream=StringIO();console=Console(file=stream,color_system=None,width=100)
    with patch.object(logo,'console',console):logo.logo('2.6',22,'neil')
    text=stream.getvalue()
    assert 'THREATHAWK' in text and 'LEGAL DISCLAIMER' in text and 'Coded by: neil' in text
    assert 'ARUGUS' not in text


def test_color_terminal_portrait_renders_from_supplied_image():
    stream=StringIO();console=Console(file=stream,color_system='truecolor',force_terminal=True,no_color=False,width=100)
    with patch.object(logo,'console',console):
        art=logo.portrait();console.print(art)
    assert '▀' in art.plain and '\x1b[' in stream.getvalue()


def test_no_color_uses_ascii_instead_of_solid_blocks():
    console=Console(file=StringIO(),color_system='truecolor',force_terminal=True,no_color=True)
    with patch.object(logo,'console',console):art=logo.portrait()
    assert '▀' not in art.plain and len(art.plain.strip())>0
