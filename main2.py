import requests
import random
import time
import getpass

def rules():
    print("\033[32mWelcome to Mastermind!\033[0m")
    print("This is a game where a player tries to guess the number combination.")
    print("Successfully guess the number code in 10 tries to win!")
    enter = input("Type '1' for single, or '2'/'3'/'4' for multiplayer humans, or 'c' vs computer: ").strip().lower()

    if enter == "1":
        level = difficulty()
        singleplayer(level)
    elif enter in {"2", "3", "4"}:
        level = difficulty()
        multiplayer_n(level, int(enter))
    elif enter == "c":
        level = difficulty()
        computer_guess(level)
    else:
        print("Try again!")
        return rules()

def multiplayer_n(level: int, num_players: int):    
    codemaker = num_players 
    secret = getpass.getpass(
        f"Player {codemaker}, secretly enter {level} numbers from 1-8 (no spaces, e.g. 1234): "
    ).strip()

    if len(secret) != level or not secret.isdigit():
        print("Try again!")
        return multiplayer_n(level, num_players)

    numbers = [int(ch) for ch in secret]
    if any(n < 1 or n > 8 for n in numbers):
        print("Try again!")
        return multiplayer_n(level, num_players)

    return game_n(numbers, level, num_players, codemaker)

def computer_guess(level):
    numbers = getpass.getpass(f"Player 2, secretly enter {level} numbers from 1-8 (no spaces, e.g. 1234): ").strip()

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
        time.sleep(3)  

        #use instead of API (rate limit)
        guess = [random.randint(1, 8) for _ in range(level)]

        print(f"\033[34mYou have {chances} chances remaining\033[0m")
        print(f"\033[34mLast guess:{guess}\033[0m")

        if guess == numbers:
            print("\033[1mComputer guessed correctly!\033[0m")
            return

        count = sum(1 for i in set(guess) if i in set(numbers))
        count2 = sum(1 for j in range(level) if guess[j] == numbers[j])
        print(f"{count} correct numbers")
        print(f"and {count2} correct locations")

        chances -= 1

    print("Computer failed to guess the code!")

def difficulty():
    level = input("Choose difficulty; Type \033[31m'3' for Easy, '4' for Normal, '5' for Difficult, or '6' for Impossible:\033[0m")
    if level in {"3", "4", "5", "6"}:
        return int(level)
    else:
        print("Try again!")
        return difficulty() 

def multiplayer(level):
    numbers = getpass.getpass(f"Player 2, secretly enter {level} numbers from 1-8 (no spaces, e.g. 1234): ").strip()
    if len(numbers) != level or not numbers.isdigit():
        print("Try again!")
        return multiplayer(level)

    numbers = [int(x) for x in numbers]
    if any(n < 1 or n > 8 for n in numbers):
        print("Try again!")
        return multiplayer(level)

    return game(numbers, level)

def singleplayer(level):
    url = "https://www.random.org/integers/"
    params = {
        "num": level,       
        "min": 1,       
        "max": 8,       
        "col": 1,       
        "base": 10,     
        "format": "plain",
        "rnd": "new"
    }

    response = requests.get(url, params=params, timeout=5)
    numbers = [int(x) for x in response.text.strip().split()]
   #deebugprint(response)
    print(numbers)  
    game(numbers, level)

def game_n(numbers, level, num_players, codemaker):
    chances = 10 * (codemaker - 1) 
    print(f"\033[34mYou have {chances} chances remaining\033[0m")

    while chances != 0:
        for p in range(1, num_players + 1):
            if p == codemaker:
                continue

            guess = input(
                f"Player {p}, enter {level} numbers from 1-8 (no spaces, e.g. 1234), there may be duplicates: "
            ).strip()

            # validate BEFORE converting
            if len(guess) != level or not guess.isdigit():
                print("Try again!")
                continue

            list1 = [int(x) for x in guess]
            if any(v < 1 or v > 8 for v in list1):
                print("Try again!")
                continue

        
            if list1 == numbers:
                print(f"\033[1mCorrect! Player {p} wins!\033[0m")
                return

            chances -= 1
            count  = sum(1 for i in set(list1) if i in set(numbers))
            count2 = sum(1 for j in range(len(list1)) if list1[j] == numbers[j])

            print(f"\033[34mYou have {chances} chances remaining\033[0m")
            print(f"\033[34mLast guess Player {p}: {list1}\033[0m")
            print(f"{count} correct numbers")
            print(f"and {count2} correct locations")

            # optional hints at 7, 4, 1 (same as your single-player)
            if chances in {7, 4, 1}:
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
                break  # out of guesses; end the outer while too

    print("Out of chances, game over!")
    print(f"Answer was: {numbers}")

def game(numbers, level): 
    chances = 10
    print(f"\033[34mYou have {chances} chances remaining\033[0m")
    while chances != 0:
        guess = input(f"Player 1, enter {level} numbers from 1-8 (no spaces, e.g. 1234), there may be duplicates: ") 
        if len(guess) != level or not guess.isdigit():
            print("Try again!")
            continue

        list1 = [int(x) for x in guess]
        if any(v < 1 or v > 8 for v in list1):
            print("Try again!")
            continue
        elif list1 == numbers:
            print("\033[1mCorrect! You win!\033[0m")
            return
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

rules()
