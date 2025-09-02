![deploy](https://github.com/luisgomez214/CMC_Thesis_Chatbot/actions/workflows/deploy.yml/badge.svg)

# Mastermind

A Python command-line implementation of the classic **Mastermind** game.  
Players attempt to guess a secret code of digits (1–8, duplicates allowed) within a limited number of tries. The game provides feedback, keeps score, and supports multiple modes.

---

## Features

-  **Game Modes**
  - Singleplayer (secret code generated randomly or via Random.org API)
  - Multiplayer (2–4 human players, rotating codemaker/guesser roles)
  - Versus CPU (computer tries to guess your code)

-  **Scoring System**
  - Tracks winners and cumulative top scores
  - Scoreboard for each round and across sessions

-  **Difficulty Levels**
  - Easy (3 digits)  
  - Normal (4 digits)  
  - Difficult (5 digits)  
  - Impossible (6 digits)

-  **Hints**
  - Strategic hints are given at certain attempt counts (e.g., count of even/odd digits, sum of digits, reveal of a random digit).

-  **Random.org Integration**
  - Fetches secret codes from [Random.org](https://www.random.org) using an API key.
  - Falls back to Python’s random number generator if desired.

---

## How to Run

Clone this repository and run from the main folder:

```bash
python3 main4.py



