import argparse

import datetime
import requests

import os
import pathlib
import importlib.util

from html_to_markdown import convert

base_url = "https://adventofcode.com/"
url_template = base_url + "{year}/day/{day}"
solution_template = """
import os

input_file_location = os.path.dirname(os.path.realpath(__file__)) + "/input.txt"

def main():
    pass
    
if __name__ == "__main__":
    main()
"""

def create_get_input_file(day_dir, url):
    """Fetches the input file for the given day and saves it in day_dir.
    Args:
        day_dir (pathlib.Path): The directory where the input file will be saved.
        url (str): The URL of the day's problem page.
    """
    dot_env_path = pathlib.Path(".env")
    if dot_env_path.exists():
        with open(dot_env_path, "r") as f:
            for line in f:
                if line.startswith("AOC_SESSION_COOKIE="):
                    _, value = line.strip().split("=", 1)
                    os.environ["AOC_SESSION_COOKIE"] = value
                    break
    session_cookie = os.getenv("AOC_SESSION_COOKIE")
    if not session_cookie:
        print(
            "AOC_SESSION_COOKIE environment variable not set. Skipping input fetch."
        )
        return
    cookies = {"session": session_cookie}
    input_url = url + "/input"
    input_response = requests.get(input_url, cookies=cookies)
    input_response.raise_for_status()
    input_data = input_response.text
    input_filename = day_dir / "input.txt"
    with open(input_filename, "w") as f:
        f.write(input_data)
    

def setup(year, day):
    for d in range(1, day + 1):
        # Create directory for the day
        day_dir = pathlib.Path(f"src/day-{d:02d}")
        day_dir.mkdir(parents=True, exist_ok=True)
        # Create empty files
        (day_dir / "__init__.py").touch()
        if not (day_dir / "solution.py").exists():
            (day_dir / "solution.py").touch()
            with open(day_dir / "solution.py", "w") as f:
                f.write(solution_template)

        # Fetch the problem description
        url = url_template.format(year=year, day=d)
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        markdown_content = convert(html_content)
        filename = day_dir / "README.md"
        with open(filename, "w") as f:
            f.write(markdown_content)

        # Fetch the input file
        if not day_dir.joinpath("input.txt").exists():
            create_get_input_file(day_dir, url)
            


def main():
    parser = argparse.ArgumentParser(description="My Advent of Code")
    subparsers = parser.add_subparsers(dest="command")
    setup_parser = subparsers.add_parser(
        "setup", help="Setup the environment for Advent of Code"
    )
    run_parser = subparsers.add_parser(
        "run", help="Run the soluction of the specified day"
    )
    run_parser.add_argument("day", type=int, help="Day to run the solution for that day (1-12)")

    args = parser.parse_args()
    
    if args.command == "setup":
        today = datetime.date.today()
        year = 2025
        day = 12
        if today.month == 12 and today.year == 2025:
            day = min(today.day, 12)

        setup(year, day)

    elif args.command == "run":
        day_dir = pathlib.Path(f"src/day-{args.day:02d}")
        if not day_dir.exists():
            print(f"Error: Day {args.day} is not set up. Please run the setup command first.")
            return
        solution_path = day_dir / "solution.py"
        spec = importlib.util.spec_from_file_location("solution", solution_path)
        if spec is None or spec.loader is None:
            print(f"Error: Could not load solution for day {args.day}")
            return
        solution = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution)
        solution.main()

    else:
        parser.print_help()
        print(f"\n{"=" * 50}\nSetup Command")
        setup_parser.print_help()
        print(f"\n{"=" * 50}\nRun Command")
        run_parser.print_help()
        
        

if __name__ == "__main__":
    main()
