import requests
import random
import getpass
import time

def countdown_timer(seconds):
    """
    Creates a countdown timer and displays the remaining time.

    Args:
        seconds (int): The duration of the timer in seconds.
    """
    t = seconds
    while t > 0:
        mins, secs = divmod(t, 60) # Convert seconds to minutes and seconds
        timer = '{:02d}:{:02d}'.format(mins, secs) # Format for display (e.g., 00:20)
        print(timer, end="\r") # Print on the same line, overwriting previous output
        time.sleep(1) # Pause for 1 second
        t -= 1 # Decrement the time
     

def rules():
    print("\033[32mWelcome to Mastermind!\033[0m")
    print("This is a game where a player tries to guess the number combination.") 
    print("The computer will provide feedback whether the player guesses a number correctly or order position correctly.")
    print("Successfully guess the number code in 10 tries to win!") 
    enter = input("Type \033[31m'1' for single player\033[0m or \033[31m'2' for multiplayer\033[0m... ")
    if enter == "1":
        level = difficulty()
        singleplayer(level) 
    elif enter == "2":
        level = difficulty()
        multiplayer(level)
    else:
        print("Try again!")
        return rules()

def difficulty():
    level = input("Choose difficulty; Type \033[31m'3' for Easy, '4' for Normal, '5' for Difficult, or '6' for Impossible:\033[0m")
    if level in {"3", "4", "5", "6"}:
        return int(level)
    else:
        print("Try again!")
        return difficulty() 

def multiplayer(level):
    numbers = getpass.getpass(
        f"Player 1, secretly enter {level} numbers from 1-8, they may duplicate if you'd like (no spaces, e.g. 1134): "
    ).strip()
    # length + digits check
    if len(numbers) != level or not numbers.isdigit():
        print("Try again!")
        return multiplayer(level)

    numbers = [int(x) for x in numbers]

    # range check 1..8
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

    response = requests.get(url, params=params)
    numbers = [int(x) for x in response.text.strip().split()]
    print(numbers)  
    game(numbers, level)

def game(numbers, level): 
    chances = 10
    print(f"\033[34mYou have {chances} chances remaining\033[0m")
    while chances != 0:
        guess = input(f"Enter {level} numbers from 1-8 (no spaces, e.g. 1234), there may be duplicates: ") 
        list1 = [int(x) for x in guess]

        if len(guess) != level or any(not x.isdigit() for x in guess) or any(list1 < 1 or list1 > 8 for list1 in numbers):
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
                        if i%2 == 0:
                            count += 1
                        elif i%2 != 0:
                            count2 += 1
                    print(f"\033[4mHint: There is {count} even numbers and {count2} odd numbers.\033[0m")
                elif chances == 1:
                    random_integer = random.randint(0, level - 1)
                    print(f"\033[4mHint: One of the numbers is {numbers[random_integer]}\033[0m")
                elif chances == 4:
                    print(f"\033[4mHint: The sum of all numbers is {sum(numbers)}\033[0m")               
    print("Out of chances, game over!")

rules()


