import sys
import json
from pathlib import Path

from rich import print
from rich.traceback import install

install(show_locals=True)

def print_file_contents(
        file_path:Path
) -> bool:
    """_summary_

    Args:
        file_path (Path): A path to the file to print out

    Returns:
        bool: True if it finishes printing to the console
    
    Note:
        Formatting codes for Rich work here too (as long as you have overridden the print function with rich's print)
    """
    try:
        with open(file_path, 'r') as f:
            for line in f.readlines():
                print(line.strip()) # stip to print verbatim content
        return True
    except FileNotFoundError, OSError:
        return False
    
print_file_contents(Path("resources/welcome_message.txt"))
# now that we welcomed the user, we should be doing something productive

user_input = input("Do you already have a server instance? [y/n]").lower().strip()
match user_input:
    case "y":
        server_path = input("Please paste the [bold]absolute[/bold] path to the exsisting server").strip()

        config_dir = Path.home() / ".justservers"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "config.json"

        with open(config_file, "w") as f:
            json.dump({"server_path": server_path}, f)

        print(f"[green]Server path saved to {config_file}[/green]")
    
    case "n":
        