# TODO: Develop a console-based Rock Paper Scissors Lizard Spock game in Python.
# The game should be modular, allowing for easy updates or rule changes.
# Implement game rules:
# - Scissors decapitate lizard
# - Scissors cuts paper
# - Paper covers rock
# - Rock crushes lizard
# - Lizard poisons Spock
# - Spock smashes scissors
# - Lizard eats paper
# - Paper disproves Spock
# - Spock vaporizes rock
# - Rock crushes scissors
# Include user input for selecting options and display game results.

import random

# ---------------------------------------------------------------------------
# Game data (change these to change the game)
# ---------------------------------------------------------------------------

# Menu number -> choice name
game_options = {
    1: "rock",
    2: "paper",
    3: "scissors",
    4: "lizard",
    5: "spock",
}

# Each choice maps to the choices it beats
game_rules = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["spock", "paper"],
    "spock": ["rock", "scissors"],
}

# Result key -> message shown to the player
game_results = {
    "win": "You win!",
    "lose": "You lose!",
    "tie": "It's a tie!",
}


# ---------------------------------------------------------------------------
# Game logic
# ---------------------------------------------------------------------------

def get_user_input():
    """Show the menu and return the player's choice name."""
    print("\nChoose your move:")
    for number, name in game_options.items():
        print(f"  {number}. {name.capitalize()}")

    while True:
        user_input = input("Enter a number (1-5): ").strip()
        # Only accept digits that are actual menu keys, so we never hit a KeyError
        if user_input.isdigit() and int(user_input) in game_options:
            return game_options[int(user_input)]
        print(f"Invalid choice '{user_input}'. Please pick a number from 1 to 5.")


def get_computer_input():
    """Return a random choice name for the computer."""
    return random.choice(list(game_options.values()))


def get_game_results(user_choice, computer_choice):
    """Return 'win', 'lose' or 'tie' from the player's point of view."""
    if user_choice == computer_choice:
        return "tie"
    if computer_choice in game_rules[user_choice]:
        return "win"
    return "lose"


def display_game_results(user_choice, computer_choice, result):
    """Print both choices and the result message."""
    print("-" * 30)
    print(f"You chose:      {user_choice.capitalize()}")
    print(f"Computer chose: {computer_choice.capitalize()}")
    print(game_results[result])
    print("-" * 30)


def main():
    print("Welcome to Rock Paper Scissors Lizard Spock!")
    user_choice = get_user_input()
    computer_choice = get_computer_input()
    result = get_game_results(user_choice, computer_choice)
    display_game_results(user_choice, computer_choice, result)


if __name__ == "__main__":
    main()
