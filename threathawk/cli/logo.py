"""Text-only ThreatHawk branding for the public distribution."""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

TEAL = "#FF6037"
console = Console()

def logo(version: str, modules: int, author: str) -> None:
    console.print(Panel(
        "⚠️ WARNING: LEGAL DISCLAIMER\n\n"
        "This tool is intended for [bold]educational and ethical use only[/bold]. "
        "The author is not liable for any illegal use or misuse of this tool. "
        "Users are solely responsible for their actions and must ensure they have "
        "explicit permission to scan the target systems.",
        border_style="yellow", title="Read before use"))
    content = Text("THREATHAWK\n", style="bold #FF6037")
    content.append("Threat intelligence · DNS · Website inspection\n\n", style="white")
    content.append(f"Version: {version}   Modules: {modules}   Coded by: {author}", style="bright_white")
    console.print(Panel(content, border_style="#FF6037", padding=(1,2)))
    console.print("Choose an option from the home menu below.", markup=False)
