from rich.console import Console
from rich.panel import Panel
from rich.text import Text

TEAL = "#2EC4B6"
console = Console()

def logo(version: str, modules: int, author: str) -> None:
    console.print(Panel(
        "⚠️ WARNING: LEGAL DISCLAIMER\n\n"
        "This tool is intended for [bold]educational and ethical use only[/bold]. "
        "The author is not liable for any illegal use or misuse of this tool. "
        "Users are solely responsible for their actions and must ensure they have "
        "explicit permission to scan the target systems.",
        border_style="yellow", title="Read before use"))
    art = r"""
                 .-------------------.
             .--'     .--------.      '--.
          .-'       .'   .--.   '.       '-.
         <         /    ( NE )    \         >
          '-.      \     '--'    /      .-'
             '--.   '--------'    .--'
                 '---------------'
    """.strip("\n")
    content = Text(art + "\n\n", style="bold cyan")
    content.append("ARUGUS BY NEIL\n", style="bold bright_white")
    content.append("Lookups & single-page checks · No intrusive scans\n\n", style="cyan")
    content.append(f"Version: {version}   Modules: {modules}   Coded by: {author}\n", style="bright_white")
    content.append("TERMINAL ONLY · No results saved to disk", style="bold green")
    console.print(Panel(content, border_style="cyan", padding=(1, 2)), justify="center")
    console.print("[cyan]Choose 1, 2, 3 or 4 from the menu below.[/cyan]")
