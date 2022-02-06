import os
from pathlib import Path

import requests

session_cookie = os.environ["SESSION_COOKIE"]
year = os.environ.get("YEAR") or 2019


for i in range(1, 26):
    url = f"https://adventofcode.com/{year}/day/{i}/input"
    with requests.get(
        url, headers={"Cookie": f"session={session_cookie}"}
    ) as request, open(
        Path(__file__).parent / f"{year}" / f"day{i}" / "input.txt", "w"
    ) as file:
        file.write(request.text)
