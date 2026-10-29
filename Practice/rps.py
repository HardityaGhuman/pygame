# TODO: Develop a console-based Rock Paper Scissors game in Python.
# The game should be modular, allowing for easy updates or rule changes.
# Implement game rules:
# - Scissors cuts paper
# - Paper covers rock
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
}

# Each choice maps to the choices it beats
game_rules = {
    "rock": ["scissors"],
    "paper": ["rock"],
    "scissors": ["paper"],
}

# Result key -> message shown to the player
game_messages = {
    "win": "You win!",
    "lose": "You lose!",
    "tie": "It's a tie!",
}


# ---------------------------------------------------------------------------
# Game logic
# ---------------------------------------------------------------------------

def is_valid_choice(user_input):
    """Return the choice name for a number or name, or None if invalid."""
    text = user_input.strip().lower()
    if text.isdigit():
        text = game_options.get(int(text), "")  # convert before validating
    return text if text in game_rules else None


def get_user_choice():
    """Show the menu and keep asking until the player gives a valid choice."""
    print("\nChoose your move:")
    for number, name in game_options.items():
        print(f"  {number}. {name.capitalize()}")

    while True:
        user_input = input(f"Enter a number (1-{len(game_options)}) or a name: ")
        choice = is_valid_choice(user_input)
        if choice:
            return choice
        print(f"Invalid choice '{user_input.strip()}'. Try again.")


def get_computer_choice():
    """Return a random choice name for the computer."""
    return random.choice(list(game_options.values()))


def determine_result(user_choice, computer_choice):
    """Return 'win', 'lose' or 'tie' from the player's point of view."""
    if user_choice == computer_choice:
        return "tie"
    if computer_choice in game_rules[user_choice]:
        return "win"
    return "lose"


def display_result(user_choice, computer_choice, result):
    """Print both choices and the result message."""
    print("-" * 30)
    print(f"You chose:      {user_choice.capitalize()}")
    print(f"Computer chose: {computer_choice.capitalize()}")
    print(game_messages[result])
    print("-" * 30)


def ask_play_again():
    """Return True if the player wants another round."""
    while True:
        answer = input("Play again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def play_game():
    """Run rounds until the player chooses to stop."""
    print("Welcome to Rock Paper Scissors!")
    while True:
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        result = determine_result(user_choice, computer_choice)
        display_result(user_choice, computer_choice, result)
        if not ask_play_again():
            break
    print("Thanks for playing!")


if __name__ == "__main__":
    try:
        play_game()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D: exit cleanly instead of showing a traceback
        print("\nGoodbye!")
