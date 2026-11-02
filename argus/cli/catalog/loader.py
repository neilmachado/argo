"""Load only the bundled reviewed catalog; ignore external catalog overrides."""
import json
from pathlib import Path
from argus.passive import ALLOWED_SCRIPTS

def minimal_fallback():
    return {}
def load():
    path = Path(__file__).resolve().parents[2] / "config" / "modules.json"
    catalog = json.loads(path.read_text())
    return {k: [m for m in v if m.get("script") in ALLOWED_SCRIPTS] for k,v in catalog.items()}
