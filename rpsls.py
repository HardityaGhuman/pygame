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

def parse_choice(user_input):
    """Turn a number or a name into a choice name, or return None if invalid.

    The number is converted to its name *before* validation, so both
    "3" and "Scissors" end up as "scissors" and go through the same check.
    """
    text = user_input.strip().lower()
    if text.isdigit():
        text = game_options.get(int(text), "")  # out-of-range number -> invalid
    return text if text in game_rules else None


def get_user_input():
    """Show the menu and return the player's choice name."""
    print("\nChoose your move:")
    for number, name in game_options.items():
        print(f"  {number}. {name.capitalize()}")

    while True:
        user_input = input(f"Enter a number (1-{len(game_options)}) or a name: ")
        choice = parse_choice(user_input)
        if choice:
            return choice
        print(f"Invalid choice '{user_input.strip()}'. Try again.")


def ask_play_again():
    """Return True if the player wants another round."""
    while True:
        answer = input("Play again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


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
    while True:
        user_choice = get_user_input()
        computer_choice = get_computer_input()
        result = get_game_results(user_choice, computer_choice)
        display_game_results(user_choice, computer_choice, result)
        if not ask_play_again():
            break
    print("Thanks for playing!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D: exit cleanly instead of showing a traceback
        print("\nGoodbye!")
