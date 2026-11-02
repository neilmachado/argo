"""ThreatHawk startup branding using Neil's supplied image."""
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

TEAL = "#FF6037"  # Compatibility name for retained view helpers.
console = Console()

def portrait():
    pixels = json.loads((Path(__file__).resolve().parents[1] / "data" / "logo.json").read_text())
    art = Text()
    ramp = " .:-=+*#%@"
    for y in range(0, len(pixels), 2):
        for top, bottom in zip(pixels[y], pixels[y + 1]):
            if console.color_system and not console.no_color:
                fg = "rgb(" + ",".join(map(str,top)) + ")"
                bg = "rgb(" + ",".join(map(str,bottom)) + ")"
                art.append("▀", style=fg + " on " + bg)
            else:
                lum = sum((top[i]+bottom[i])*w for i,w in enumerate((0.2126,0.7152,0.0722))) / 2
                art.append(ramp[min(9,int(lum / 256 * 10))])
        art.append("\n")
    return art

def logo(version: str, modules: int, author: str) -> None:
    console.print(Panel(
        "⚠️ WARNING: LEGAL DISCLAIMER\n\n"
        "This tool is intended for [bold]educational and ethical use only[/bold]. "
        "The author is not liable for any illegal use or misuse of this tool. "
        "Users are solely responsible for their actions and must ensure they have "
        "explicit permission to scan the target systems.",
        border_style="yellow", title="Read before use"))
    content = portrait()
    content.append("\nTHREATHAWK\n", style="bold #FF6037")
    content.append("Threat intelligence · DNS · Website inspection\n\n", style="white")
    content.append(f"Version: {version}   Modules: {modules}   Coded by: {author}\n", style="bright_white")
    content.append("TERMINAL ONLY · No results saved to disk", style="green")
    console.print(Panel(content, border_style="#FF6037", padding=(1,2)))
    console.print("Choose an option from the home menu below.", markup=False)
