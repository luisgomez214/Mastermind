# .github/workflows/random.py
from pathlib import Path

OUT = Path("guesses.txt")
guess = "1234"

lines = [guess for _ in range(10)]          # exactly 10 tries
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")  # ensure trailing newline
print("Wrote guesses to guesses.txt")

