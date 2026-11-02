"""Four-option guided terminal menu. No command syntax to memorize."""
import base64
import binascii
import ipaddress
import json
import requests
from urllib.parse import urlsplit
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from argo.cli.catalog.loader import load
from argo.cli.logo import logo
from argo.config.settings import API_KEYS
from argo.passive import ALLOWED_SCRIPTS, ProviderError, domain, otx_indicator, lookup as record_lookup
from argo.nonintrusive import RESTORED, WEB, PATHS, lookup as restored_lookup, website_url

INPUT_LABELS = {
    "otx_indicator": "IP address, domain, or MD5/SHA-1/SHA-256 hash",
    "domain": "Domain name",
    "ip": "IPv4 or IPv6 address",
    "domain_or_ip": "Domain name or IP address",
    "website": "Website domain or HTTP(S) origin",
    "jwt": "JWT token (decoded offline)",
}

def modules():
    return [m for entries in load().values() for m in entries]

def validate_input(module, value):
    value = value.strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    kind = module["input_type"]
    if kind == "otx_indicator":
        return otx_indicator(value)[1]
    if kind == "domain":
        return domain(value)
    if kind == "ip":
        try:
            return str(ipaddress.ip_address(value))
        except ValueError:
            raise ValueError("Enter an IP address, for example 8.8.8.8. A domain or email is not accepted.") from None
    if kind == "domain_or_ip":
        try:
            return str(ipaddress.ip_address(value))
        except ValueError:
            return domain(value)
    if kind == "website":
        website_url(value)  # Validation only; no request made here.
        return value
    if kind == "jwt":
        if len(value) > 65536:
            raise ValueError("JWT token is too large.")
        parts = value.split(".")
        if len(parts) != 3:
            raise ValueError("Paste a three-part JWT: header.payload.signature.")
        try:
            decoded = [json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4))) for p in parts[:2]]
            if not all(isinstance(p, dict) for p in decoded):
                raise ValueError()
        except (ValueError, UnicodeError, binascii.Error):
            raise ValueError("JWT header and payload must contain valid base64url JSON objects.") from None
        return value
    raise ValueError("Unsupported input type.")

def redirect_origin(current, result, script):
    """Offer one explicit retry only for the same site's HTTPS origin/www alias."""
    if script not in WEB or not isinstance(result, dict) or not 300 <= result.get('status', 0) < 400:
        return None
    try:
        source = urlsplit(website_url(current))
        target = urlsplit(result.get('redirect_to', ''))
        if target.scheme != 'https' or target.query or target.fragment or target.username or target.password:
            return None
        if target.port not in (None, 443) or target.path not in ('', '/', PATHS.get(script, '/')):
            return None
        source_host = (source.hostname or '').lower()
        target_host = (target.hostname or '').lower()
        if source_host.removeprefix('www.') != target_host.removeprefix('www.'):
            return None
        destination = 'https://' + target.netloc
        website_url(destination)
        if destination.rstrip('/') == (source.scheme + '://' + source.netloc).rstrip('/'):
            return None
        return destination
    except ValueError:
        return None

class Menu:
    def __init__(self, console=None, read=None):
        self.console = console or Console()
        self.read = read or input
        self.items = modules()
        self.selected = None
        self.redirect_target = None

    def show_menu(self):
        selected = self.selected["name"] if self.selected else "None — choose 2 to select a module"
        self.console.print(Text("Selected: " + selected, style="cyan"))
        self.console.print(Panel(
            "1. View modules\n2. Select module\n3. Run module\n4. Exit",
            title="Argo", border_style="#FF6037", expand=False))

    def view_modules(self):
        table = Table(title=f"Modules 1–{len(self.items)}", header_style="bold cyan", show_lines=False)
        table.add_column("No.", justify="right", no_wrap=True)
        table.add_column("Module")
        table.add_column("Required input")
        table.add_column("API / source")
        for m in self.items:
            table.add_row(f'{int(m["id"]):02}', m["name"], INPUT_LABELS[m["input_type"]], m["source"])
        self.console.print(table)

    def details(self):
        m = self.selected
        text = Text(f'{int(m["id"]):02}. {m["name"]}\n\n', style="bold cyan")
        text.append(m["description"] + "\n\n", style="white")
        text.append(m["source"] + "\n" + m["source_details"] + "\n\n", style="white")
        text.append("Required input: " + INPUT_LABELS[m["input_type"]] + "\n", style="bold white")
        text.append("Example: " + m["example"] + "\n", style="green")
        credential = m.get("api_key")
        text.append("API key: " + (credential + (" — configured" if API_KEYS.get(credential) else " — missing") if credential else "Not required"))
        if m["input_type"] == "domain":
            text.append("\nEnter only the domain, without https://, paths or an email address.")
        elif m["input_type"] == "website":
            text.append("\nOne GET only. No crawling, redirects or form submissions. Use a site you are permitted to check.")
        elif m["input_type"] == "jwt":
            text.append("\nOffline decoding only; signature and claims are not verified.")
        self.console.print(Panel(text, title="Selected module", border_style="#FF6037"))

    def select_module(self):
        number = self.read(f"Enter module number (1–{len(self.items)}), b to go home, or q to exit: ").strip()
        if number.lower() == "q":
            return "exit"
        if number.lower() == "b":
            return "back"
        if not number:
            return "back"
        if not number.isascii() or not number.isdigit():
            self.console.print(f"Enter a module number between 1 and {len(self.items)}.", markup=False)
            return
        match = next((m for m in self.items if int(m["id"]) == int(number)), None)
        if not match:
            self.console.print(f"That module does not exist. Choose a number between 1 and {len(self.items)}.", markup=False)
            return
        self.selected = match
        self.redirect_target = None
        self.details()
        return "selected"

    def run_module(self, value=None):
        self.redirect_target = None
        if not self.selected:
            self.console.print("Select a module before running.", markup=False)
            return
        m = self.selected
        credential = m.get("api_key")
        if credential and not API_KEYS.get(credential):
            self.console.print("Missing " + credential + ". Configure it in your local environment and restart the tool.", markup=False)
            return
        self.console.print(m["source"], markup=False)
        self.console.print(m["source_details"], markup=False)
        self.console.print("Required input: " + INPUT_LABELS[m["input_type"]], markup=False)
        self.console.print("Example: " + m["example"], markup=False)
        if value is None:
            value = self.read("Enter input (Enter to cancel): ")
        if not value.strip():
            return
        try:
            value = validate_input(m, value)
        except ValueError as exc:
            self.console.print("Invalid input: " + str(exc), markup=False)
            return
        script = m["script"]
        if script not in ALLOWED_SCRIPTS:
            self.console.print("Module blocked: not in the reviewed allowlist.", markup=False)
            return
        try:
            self.console.print(Text("Running " + m["name"] + "…", style="cyan"))
            result = restored_lookup(script, value) if script in RESTORED else record_lookup(script, value)
            self.redirect_target = redirect_origin(value, result, script)
            self.console.print_json(data=result)
            if isinstance(result, dict) and result.get("outcome") == "not_analyzed":
                if self.redirect_target:
                    self.console.print('Website moved to ' + self.redirect_target + '. Type r below to make one separate request to that same-site destination, if permitted.', markup=False)
                elif result.get('status') == 403:
                    self.console.print('Access denied by the website (HTTP 403). No analysis was possible; no bypass will be attempted.', markup=False)
                else:
                    self.console.print("Not analyzed. See the HTTP status and next-step guidance above.", markup=False)
            else:
                self.console.print("Finished. Results were displayed only in this terminal.", markup=False)
        except requests.exceptions.Timeout:
            self.console.print("The remote service timed out. No result was obtained; try again later.", markup=False)
        except requests.exceptions.SSLError:
            self.console.print("TLS certificate verification failed. The request was stopped; do not disable verification to bypass this.", markup=False)
        except requests.exceptions.ConnectionError:
            self.console.print("Could not connect to the remote service. Check your connection or try again later.", markup=False)
        except ProviderError as exc:
            self.console.print(str(exc), markup=False)
        except KeyboardInterrupt:
            self.console.print("Run cancelled.", markup=False)
        except Exception as exc:
            # Do not expose request URLs, provider bodies, input tokens or API keys.
            self.console.print("Lookup failed (" + type(exc).__name__ + "). Check connectivity, input and provider access.", markup=False)

    def run(self):
        section = "home"
        while True:
            try:
                if section == "home":
                    self.show_menu()
                    choice = self.read("Choose an option (1–4): ").strip()
                    if choice in ("1", "2"):
                        self.view_modules()
                        section = "select"
                    elif choice == "3":
                        if self.selected:
                            self.run_module()
                            section = "result"
                        else:
                            self.console.print("Select a module before running.", markup=False)
                            self.view_modules()
                            section = "select"
                    elif choice == "4":
                        break
                    else:
                        self.console.print("Please enter 1, 2, 3 or 4.", markup=False)
                elif section == "select":
                    action = self.select_module()
                    if action == "exit": break
                    if action == "back": section = "home"
                    elif action == "selected": section = "ready"
                else:
                    name = self.selected["name"]
                    redirect_hint = ("; r to check " + self.redirect_target) if self.redirect_target else ""
                    action = self.read(
                        ("Enter input to run " if section == "ready" else "Enter new input to run again: ")
                        + name + " (or press Enter for guidance)" + redirect_hint + "; b for home; q to exit: "
                    ).strip()
                    if action.lower() == "q": break
                    if action.lower() == "b":
                        section = "home"
                    elif action.lower() == "r" and self.redirect_target:
                        self.run_module(value=self.redirect_target)
                        section = "result"
                    elif action == "":
                        self.run_module()
                        section = "result"
                    else:
                        self.run_module(value=action)
                        section = "result"
            except EOFError:
                break
            except KeyboardInterrupt:
                self.console.print("Action cancelled.", markup=False)
        self.console.print("Goodbye — Argo.", markup=False)

def main():
    menu = Menu()
    logo("2.6.1", len(menu.items), "neil")
    menu.run()
