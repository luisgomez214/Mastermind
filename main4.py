import requests
import random
import sys, time, threading, queue
import signal
import getpass
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()  

RANDOM_ORG_API_KEY = os.getenv("RANDOM_ORG_API_KEY")
RANDOM_ORG_URL = "https://api.random.org/json-rpc/4/invoke"
REQUIRE_RANDOM_ORG = True  

WINNERS = []  
SCORES = [] 
ROUND_BREAK = "__ROUND_BREAK__" 

def show_highscores():
    print("\n\033[33m--- Cumulative Top Scores ---\033[0m")

    totals = {}
    cur_best = {}

    for entry in SCORES + [ROUND_BREAK]:   
        if entry == ROUND_BREAK:
            for name, best in cur_best.items():
                totals[name] = totals.get(name, 0) + best
            cur_best = {}
            continue
        try:
            name, val_str = entry.split(" score:")
            val = int(val_str)
        except ValueError:
            continue
        cur_best[name] = max(cur_best.get(name, 0), val)

    if not totals:
        print("(no scores yet)")
        return

    for name in sorted(totals):
        print(f"{name} Score: {totals[name]}")

def show_scoreboard():
    if not WINNERS:
        print("\n\033[33m--- Scoreboard ---\033[0m\n(no games yet)\n")
        return
    tally = Counter(WINNERS)
    print("\n\033[33m--- Scoreboard ---\033[0m")
    for name in sorted(tally):  # simple alphabetical
        print(f"{name}: {tally[name]}")
    print()

def rules():
    print("\033[32mWelcome to Mastermind!\033[0m")
    print("This is a game where a player tries to guess the number combination.")
    print("Successfully guess the number code in 10 tries to win!")
    enter = input("Type '1' for single, or '2'/'3'/'4' for multiplayer humans, 'c' vs computer, or 'q' to quit: ").strip().lower()

    if enter == "1":
        level = difficulty()
        singleplayer(level)
    elif enter in {"2", "3", "4"}:
        level = difficulty()
        multiplayer_rotating_session(level, int(enter))
    elif enter == "c":
        level = difficulty()
        computer_guess(level)
    elif enter == "q":
        print("Goodbye!")
        return "QUIT" 
    else:
        print("Try again!")
        return rules()

def _get_secret(level: int, codemaker: int):
    secret = getpass.getpass(
        f"Player {codemaker}, secretly enter {level} numbers from 1-8 (no spaces, e.g. 1234): "
    ).strip()
    if len(secret) != level or not secret.isdigit():
        print("Try again!")
        return _get_secret(level, codemaker)
    nums = [int(ch) for ch in secret]
    if any(n < 1 or n > 8 for n in nums):
        print("Try again!")
        return _get_secret(level, codemaker)
    return nums

def multiplayer_rotating_session(level: int, num_players: int):
    codemaker = 1  # start with Player 1 as codemaker (change if you prefer)
    while True:
        numbers = _get_secret(level, codemaker)
        game_n(numbers, level, num_players, codemaker)  
        show_scoreboard()
        codemaker = (codemaker % num_players) + 1
        
        while True:
            choice = input("Enter to play next round, or 'm' to return to menu: ").strip().lower()
            if choice == "m":
                WINNERS.clear()
                SCORES.clear()
                break
            if choice == "":
                SCORES.append(ROUND_BREAK)
                break
            print("Try again!")


def computer_guess(level):
    while True:
        numbers = getpass.getpass(f"Player 1, secretly enter {level} numbers from 1-8 (no spaces, e.g. 1234): ").strip()

        if len(numbers) != level or not numbers.isdigit():
            print("Try again!")
            return computer_guess(level)

        numbers = [int(x) for x in numbers]
        if any(n < 1 or n > 8 for n in numbers):
            print("Try again!")
            return computer_guess(level)

        print("\033[32mComputer will now try to guess your code...\033[0m")

        chances = 10
        while chances > 0:
            time.sleep(.1)  

            #use instead of API for testing 
            guess = [random.randint(1, 8) for _ in range(level)]
            count = sum(1 for i in set(guess) if i in set(numbers))
            count2 = sum(1 for j in range(level) if guess[j] == numbers[j])
            print(f"\033[34mYou have {chances} chances remaining\033[0m")
            print(f"\033[34mLast guess:{guess}\033[0m")
            score = count + count2

            if guess == numbers:
                print(f"{count} correct numbers")
                print(f"and {count2} correct locations")
                print("\033[1mComputer guessed correctly!\033[0m")
                SCORES.append(f"CPU score:{score}")
                WINNERS.append("CPU")
                show_scoreboard()
                show_highscores()
            
            while True:
                choice = input("Enter to play next round, or 'm' to return to menu: ").strip().lower()
                if choice == "m":
                    WINNERS.clear()
                    SCORES.clear()
                    break
                if choice == "":
                    SCORES.append(ROUND_BREAK)
                    break
                print("Try again!")
                
            print(f"{count} correct numbers")
            print(f"and {count2} correct locations")
            
            print(f"\033[37mCPU score this guess: {score}\033[0m")
            SCORES.append(f"CPU score:{score}")

            chances -= 1

        print("Computer failed to guess the code!")
        WINNERS.append("Player 1")
        show_scoreboard()
        show_highscores()
        while True:
            choice = input("Enter to play next round, or 'm' to return to menu: ").strip().lower()
            if choice == "m":
                WINNERS.clear()
                SCORES.clear()
                break
            if choice == "":
                SCORES.append(ROUND_BREAK)
                break
            print("Try again!")

def difficulty():
    level = input("Choose difficulty; Type \033[31m'3' for Easy, '4' for Normal, '5' for Difficult, or '6' for Impossible:\033[0m")
    if level in {"3", "4", "5", "6"}:
        return int(level)
    else:
        print("Try again!")
        return difficulty() 

def fetch_secret_from_random_org(level: int, timeout: int = 5) -> list[int]:
    if not RANDOM_ORG_API_KEY:
        raise RuntimeError("Missing env var RANDOM_ORG_API_KEY")

    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": RANDOM_ORG_API_KEY,
            "n": level,
            "min": 1,
            "max": 8,
            "replacement": True
        },
        "id": 1
    }

    r = requests.post(RANDOM_ORG_URL, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()

    if "error" in data:
        code = data["error"].get("code")
        msg  = data["error"].get("message")
        raise RuntimeError(f"Random.org error {code}: {msg}")

    nums = data["result"]["random"]["data"]
    if not isinstance(nums, list) or len(nums) != level:
        raise RuntimeError(f"Unexpected response: {data}")
    if any(not isinstance(x, int) or x < 1 or x > 8 for x in nums):
        raise RuntimeError(f"Out-of-range integers: {nums}")
    return nums

def singleplayer(level):
    while True:
        try:
            numbers = fetch_secret_from_random_org(level)
        except Exception as e:
            print(f"Random.org failed: {e}")
            if REQUIRE_RANDOM_ORG:
                print("Returning to menu (API key required).")
                break
            print("Using local RNG fallback.")

        game(numbers, level)

        while True:
            choice = input("Enter to play next round, or 'm' to return to menu: ").strip().lower()
            if choice == "m":
                WINNERS.clear()
                SCORES.clear()
                break
            if choice == "":
                SCORES.append(ROUND_BREAK)
                break 
            print("Try again!")

def game_n(numbers, level, num_players, codemaker):
    chances = 5 
    print(f"\033[34mYou have {chances} chances remaining\033[0m")
    while chances != 0:
        for p in range(1, num_players + 1):
            if p == codemaker:
                continue
            
            guess = input(
                f"Player {p}, enter {level} numbers from 1-8 (no spaces, e.g. 1234), there may be duplicates: "
            ).strip()
            

            if len(guess) != level or not guess.isdigit():
                print("Try again!")
                continue

            list1 = [int(x) for x in guess]
            if any(v < 1 or v > 8 for v in list1):
                print("Try again!")
                continue
        
            chances -= 1
            count  = sum(1 for i in set(list1) if i in set(numbers))
            count2 = sum(1 for j in range(len(list1)) if list1[j] == numbers[j])

            print(f"\033[34mYou have {chances} chances remaining \033[0m")
            print(f"\033[34mLast guess Player {p}: {list1}\033[0m")
            print(f"{count} correct numbers")
            print(f"and {count2} correct locations")

            score = count + count2
            print(f"\033[37mYour score this guess: {score}\033[0m")
            SCORES.append(f"Player {p} score:{score}")

            if list1 == numbers:
                print("\033[1mCorrect! You win!\033[0m")
                WINNERS.append(f"Player {p}")
                show_scoreboard()
                show_highscores()
                return 

            if chances in {7,4,1}:
                if chances == 7:
                    evens = sum(1 for n in numbers if n % 2 == 0)
                    odds  = len(numbers) - evens
                    print(f"\033[4mHint: There are {evens} even and {odds} odd numbers.\033[0m")
                elif chances == 4:
                    print(f"\033[4mHint: The sum of all numbers is {sum(numbers)}\033[0m")
                elif chances == 1:
                    idx = random.randint(0, level - 1)
                    print(f"\033[4mHint: One of the numbers is {numbers[idx]}\033[0m")

            if chances == 0:
                break  

    print("Out of chances, game over!")
    print(f"Answer was: {numbers}")
    WINNERS.append(f"Player {codemaker}") 
    show_highscores()

def game(numbers, level): 
    print(numbers)
    chances = 10
    print(f"\033[34mYou have {chances} chances remaining\033[0m")
    while chances != 0:
        guess = input(f"Player 1, enter {level} numbers from 1-8 (no spaces, e.g. 1234), there may be duplicates: ") 
        if len(guess) != level or not guess.isdigit():
            print("Try again!")
            continue

        if len(guess) != level or not guess.isdigit():
            print("Try again!")
            continue

        list1 = [int(x) for x in guess]
        if any(v < 1 or v > 8 for v in list1):
            print("Try again!")
            continue
        else:
            chances -= 1
            count = 0   # correct numbers (anywhere)
            count2 = 0  # correct numbers in correct location

            print(f"\033[34mYou have {chances} chances remaining\033[0m")
            print(f"\033[34mLast guess:{list1}\033[0m")
            for i in list(set(list1)):
                if i in list(set(numbers)):
                    count += 1
            print(f"{count} correct numbers")

            for j in range(len(list1)):
                if list1[j] == numbers[j]:
                    count2 += 1 
            print(f"and {count2} correct locations")
            
            score = count + count2
            print(f"\033[37mYour score this guess: {score}\033[0m")
            SCORES.append(f"Player 1 score:{score}")
            
        if list1 == numbers:
            print("\033[1mCorrect! You win!\033[0m")
            WINNERS.append(f"Player 1")
            show_scoreboard()
            show_highscores()
            return

        if chances in {7, 4, 1}:
            if chances == 7:
                count, count2 = 0, 0
                for i in numbers:
                    if i % 2 == 0:
                        count += 1
                    elif i % 2 != 0:
                        count2 += 1
                print(f"\033[4mHint: There is {count} even numbers and {count2} odd numbers.\033[0m")
            elif chances == 1:
                random_integer = random.randint(0, level - 1)
                print(f"\033[4mHint: One of the numbers is {numbers[random_integer]}\033[0m")
            elif chances == 4:
                print(f"\033[4mHint: The sum of all numbers is {sum(numbers)}\033[0m")               

            
    print("Out of chances, game over!")
    WINNERS.append("CPU") 
    show_scoreboard()
    show_highscores()

if __name__ == "__main__":
    while True:
        if rules() == "QUIT":
            break
