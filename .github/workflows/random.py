import requests
from pathlib import Path

OUT = Path("guesses.txt")
lines = []

for _ in range(10):  # 10 guesses
    url = "https://www.random.org/integers/"
    params = {
        "num": 4,
        "min": 0,
        "max": 7,
        "col": 1,
        "base": 10,
        "format": "plain",
        "rnd": "new"
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    nums = [x for x in r.text.strip().split()]  # 4 lines → 4 tokens
    lines.append(" ".join(nums))

OUT.write_text("\n".join(lines), encoding="utf-8")
print("Wrote guesses to guesses.txt")

