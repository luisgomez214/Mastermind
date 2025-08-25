from pathlib import Path

OUT = Path("guesses.txt")

# Define the guess you want to repeat
guess = "1234"

# Repeat it 10 times
lines = [guess for _ in range(10)]

# Save to file
OUT.write_text("\n".join(lines), encoding="utf-8")
print("Wrote guesses to guesses.txt")

