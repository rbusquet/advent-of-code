import datetime
import os
from pathlib import Path

import requests

session_cookie = os.environ["SESSION_COOKIE"]
year = os.environ.get("YEAR") or 2019

today = datetime.date.today()

for i in range(1, 26):
    if today.day > i:
        break
    url = f"https://adventofcode.com/{year}/day/{i}/input"
    headers = {"Cookie": f"session={session_cookie}"}
    out_file = Path(__file__).parent / f"{year}" / f"day_{i:0>2}" / "input.txt"
    with (
        requests.get(url, headers=headers) as request,
        open(out_file, "w") as file,
    ):
        file.write(request.text)
