import requests

def rules():
    print("\033[1mWelcome to Mastermind!\033[0m")
    print("This is a game where a player tries to guess the number combinations.") 
    print("The computer will provide feedback whether the player guesses a number correctly or order position correctly.")
    print("Successfully guess the 4 number code in 10 tries to win!") 
    enter = input("Type '1' for single player or '2' for multiplayer... ")
    if enter == "1":
        singleplayer() 
    elif enter == "2":
        multiplayer()
    else:
        raise ValueError("Try again!")

def multiplayer():
    numbers = input("Player 1, secretly enter 4 numbers from 0-7, they may be duplicates (no spaces, e.g. 1234): ")
    numbers = [int(x) for x in numbers]
    game(numbers)
    
def singleplayer():
    url = "https://www.random.org/integers/"
    params = {
        "num": 4,       # number of integers
        "min": 0,       # minimum value
        "max": 7,       # maximum value
        "col": 1,       # one per line
        "base": 10,     # decimal
        "format": "plain",
        "rnd": "new"
    }

    response = requests.get(url, params=params)
    print(response) 
    numbers = [int(x) for x in response.text.strip().split()]
    print(numbers)  # e.g. [3, 0, 7, 5
    game(numbers)

def game(numbers): 
    chances = 10
    while chances != 0:
        guess = input("Enter 4 numbers from 0-7 (no spaces, e.g. 1234), they may be duplicates: ") 
        list1 = [int(x) for x in guess]

        if len(guess) != 4 or any(not x.isdigit() for x in guess):
            print("Try again!")
            continue 
        elif list1 == numbers:
            print("Correct! You win!")
            return
        else:
            chances -= 1
            count = 0   # correct numbers (anywhere)
            count2 = 0  # correct numbers in correct location
            print(f"You have {chances} chances remaining")
            print(f"Last guess:{list1}")
            for i in list1:
                if i in numbers:
                    count += 1
            print(f"{count} correct numbers")

            for j in range(len(list1)):
                if list1[j] == numbers[j]:
                    count2 += 1 
            print(f"and {count2} correct locations")
    print("Out of chances, game over!")

rules()

