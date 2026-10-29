"""Castle text adventure.

The player walks through randomly chosen rooms in a castle. Each room runs an
Encounter, which returns an EncounterOutcome telling the game whether to keep
going (CONTINUE) or stop (END).

To add a new kind of encounter: subclass Encounter, implement run_encounter,
and add a Room that uses it to the `rooms` list.
"""

import random
from abc import ABC, abstractmethod
from enum import Enum


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

# Hints at past events, from grand to subtle. Each fits any room.
clues = [
    "There is a scorch mark across the floor, as if a great fire once raged here.",
    "There is a shattered sword lying in the corner, its blade snapped in two.",
    "There is a faded banner on the wall, torn by something with long claws.",
    "There is a dried bloodstain on the flagstones, partly scrubbed away.",
    "There is a toppled chair, as though someone left in a terrible hurry.",
    "There is a half-burned letter in the hearth, its signature still legible.",
    "There is a single glove on the floor, embroidered with a royal crest.",
    "There is a goblet on its side, the wine inside long since dried to a stain.",
    "There is a small key hidden in a crack between the stones.",
    "There is a child's wooden toy, worn smooth by years of handling.",
]

# Sensory descriptions (sight, sound, smell, touch, intuition) for any room.
sense_exp = [
    "You see shadows flicker on the walls, though no candle is lit.",
    "You see dust motes hanging motionless in a shaft of pale light.",
    "You see your breath mist in the air, despite the summer outside.",
    "You hear faint footsteps echoing from somewhere above you.",
    "You hear a distant chime, like a bell rung underwater.",
    "You hear whispering that stops the moment you hold your breath.",
    "You smell old smoke and damp stone.",
    "You smell lavender, sweet and out of place.",
    "You feel a cold draft brush the back of your neck.",
    "You feel the floor tremble very slightly beneath your feet.",
    "You sense that someone has been watching you since you entered.",
    "You sense that this room remembers something it would rather forget.",
]


# ---------------------------------------------------------------------------
# Random selection
# ---------------------------------------------------------------------------

class RandomItemSelector:
    """Pick random items without repeats until every item has been used."""

    def __init__(self, items):
        self.items = list(items)  # copy so the caller's list isn't modified
        self.used_items = []

    def add_item(self, item):
        """Add an item to the selection pool."""
        self.items.append(item)

    def pull_random_item(self):
        """Return a random unused item, or None if there are no items at all.

        When every item has been used, the used list is reset first.
        A list comprehension (not a set) is used so this works for unhashable
        items and keeps the original order.
        """
        if not self.items:
            return None

        available = [item for item in self.items if item not in self.used_items]
        if not available:
            self.reset()
            available = list(self.items)

        item = random.choice(available)
        self.used_items.append(item)
        return item

    def reset(self):
        """Make all items available again."""
        self.used_items = []


class SenseClueGenerator:
    """Singleton that combines a random clue with a random sensory line."""

    _instance = None

    def __new__(cls, clue_list=None, sense_list=None):
        # Only the first call builds the selectors; later calls reuse them.
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.clue_selector = RandomItemSelector(
                clue_list if clue_list is not None else clues
            )
            cls._instance.sense_selector = RandomItemSelector(
                sense_list if sense_list is not None else sense_exp
            )
        return cls._instance

    def get_senseclue(self):
        """Return a short description made of one sense line and one clue."""
        clue = self.clue_selector.pull_random_item()
        sense = self.sense_selector.pull_random_item()
        return f"{sense}\n{clue}"


# ---------------------------------------------------------------------------
# Encounters
# ---------------------------------------------------------------------------

class EncounterOutcome(Enum):
    CONTINUE = "continue"
    END = "end"


class Encounter(ABC):
    """Base class for everything that can happen in a room."""

    @abstractmethod
    def run_encounter(self) -> EncounterOutcome:
        """Run the encounter and return an EncounterOutcome."""


class DefaultEncounter(Encounter):
    """Describe the room's atmosphere and let the player move on."""

    def __init__(self):
        self.sense_clue_generator = SenseClueGenerator(clues, sense_exp)

    def run_encounter(self):
        print(self.sense_clue_generator.get_senseclue())
        return EncounterOutcome.CONTINUE


class TreasureEncounter(Encounter):
    """The win condition: finding the treasure ends the game."""

    def run_encounter(self):
        print("Gold coins and jewels glitter in the torchlight.")
        print("*** You found the treasure! You have won the game! ***")
        return EncounterOutcome.END


class RedWizardEncounter(Encounter):
    """A spell battle against the Red Wizard.

    Each spell beats two others and loses to two. A draw replays the round.
    Player wins -> the wizard is vanquished and the game CONTINUEs.
    Wizard wins -> the player is vanquished and the game ENDs.
    """

    wizard_name = "Red Wizard"

    # Each spell maps to the spells it beats
    game_rules = {
        "Fireball": ["Ice Shard", "Lightning Bolt"],
        "Ice Shard": ["Wind Gust", "Earthquake"],
        "Wind Gust": ["Lightning Bolt", "Fireball"],
        "Lightning Bolt": ["Earthquake", "Ice Shard"],
        "Earthquake": ["Fireball", "Wind Gust"],
    }

    # (winning spell, losing spell) -> how the winner overpowers the loser
    win_verbs = {
        ("Fireball", "Ice Shard"): "melts",
        ("Fireball", "Lightning Bolt"): "consumes",
        ("Ice Shard", "Wind Gust"): "freezes",
        ("Ice Shard", "Earthquake"): "seals the cracks of",
        ("Wind Gust", "Lightning Bolt"): "scatters",
        ("Wind Gust", "Fireball"): "snuffs out",
        ("Lightning Bolt", "Earthquake"): "splits",
        ("Lightning Bolt", "Ice Shard"): "shatters",
        ("Earthquake", "Fireball"): "buries",
        ("Earthquake", "Wind Gust"): "grounds",
    }

    def get_player_spell(self):
        """Show the spells and return a valid one (number or name, any case)."""
        spells = list(self.game_rules)
        # Lower-case lookup so "ice shard", "ICE  SHARD" etc. all match "Ice Shard"
        by_name = {spell.lower(): spell for spell in spells}

        print("\nYour spellbook:")
        for number, spell in enumerate(spells, start=1):
            print(f"  {number}. {spell}")

        while True:
            raw = input(f"Cast a spell (1-{len(spells)} or name): ")
            text = " ".join(raw.split()).lower()  # trim and collapse spaces
            if text.isdigit() and 1 <= int(text) <= len(spells):
                return spells[int(text) - 1]
            if text in by_name:
                return by_name[text]
            print(f"  '{raw.strip()}' is not a spell you know. Try again.")

    def describe_win(self, winner, loser):
        """Return a line like 'Fireball melts Ice Shard'."""
        verb = self.win_verbs.get((winner, loser), "overpowers")
        return f"{winner} {verb} {loser}"

    def run_encounter(self):
        print(f"The {self.wizard_name} raises a staff crackling with power.")
        print("A spell battle begins!")
        round_number = 1
        while True:
            print(f"\n--- Round {round_number} ---")
            player_spell = self.get_player_spell()
            wizard_spell = random.choice(list(self.game_rules))
            # Pad both labels to the same width so the spell names line up
            wizard_label = f"The {self.wizard_name} casts:"
            width = len(wizard_label)
            print(f"\n  {'You cast:':<{width}} {player_spell}")
            print(f"  {wizard_label} {wizard_spell}")

            if player_spell == wizard_spell:
                # Draw: the spells cancel out, so play another round
                print("  The spells collide and cancel out!")
                round_number += 1
                continue

            if wizard_spell in self.game_rules[player_spell]:
                # The player's spell beats the wizard's spell
                print(f"  {self.describe_win(player_spell, wizard_spell)}!")
                print(f"\nThe {self.wizard_name} has been vanquished from this castle!")
                return EncounterOutcome.CONTINUE

            # Otherwise the wizard's spell beats the player's spell
            print(f"  {self.describe_win(wizard_spell, player_spell)}!")
            print("\nYou have been vanquished from this castle!")
            return EncounterOutcome.END


# ---------------------------------------------------------------------------
# Rooms and castle
# ---------------------------------------------------------------------------

class Room:
    """A named room with one encounter."""

    def __init__(self, name, encounter):
        self.name = name
        self.encounter = encounter

    def visit_room(self):
        """Run this room's encounter and return its outcome."""
        return self.encounter.run_encounter()


rooms = [
    Room("Throne Room", DefaultEncounter()),
    Room("Armory", DefaultEncounter()),
    Room("Library", DefaultEncounter()),
    Room("Dungeon", DefaultEncounter()),
    Room("Observatory", DefaultEncounter()),
    Room("Royal Chamber", DefaultEncounter()),
    Room("Treasure Room", TreasureEncounter()),
    Room("The Red Wizard's Lair", RedWizardEncounter()),
]


class Castle:
    """Lets the player pick a door, then visits a random room behind it."""

    MIN_DOORS = 2
    MAX_DOORS = 4

    def __init__(self, room_list):
        self.room_selector = RandomItemSelector(room_list)

    def select_door(self):
        """Show a random number of doors and return the player's valid pick."""
        door_count = random.randint(self.MIN_DOORS, self.MAX_DOORS)
        print(f"\nYou see {door_count} doors in front of you.")

        while True:
            choice = input(f"Which door will you open? (1-{door_count}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= door_count:
                return int(choice)
            print(f"  '{choice}' is not a door. Enter a number from 1 to {door_count}.")

    def next_room(self):
        """Pick a door, enter a random room and return the encounter outcome."""
        door = self.select_door()
        room = self.room_selector.pull_random_item()
        if room is None:
            # Empty room list: nothing to explore, so end instead of crashing.
            print("The castle is empty.")
            return EncounterOutcome.END

        # Avoid "the The Red Wizard's Lair" for names that already start with "The"
        place = room.name if room.name.startswith("The ") else f"the {room.name}"
        print(f"\nYou open door {door} and step into {place}.")
        print("=" * 50)
        outcome = room.visit_room()
        print("=" * 50)
        return outcome

    def reset(self):
        """Make every room available again."""
        self.room_selector.reset()


# ---------------------------------------------------------------------------
# Game
# ---------------------------------------------------------------------------

class Game:
    """Main loop: keep visiting rooms until an encounter ends the game."""

    def __init__(self, room_list):
        self.castle = Castle(room_list)

    def play_game(self):
        print("=" * 50)
        print("Welcome to the Castle!")
        print("Navigate the castle and find the treasure to win.")
        print("=" * 50)

        while True:
            outcome = self.castle.next_room()
            if outcome == EncounterOutcome.END:
                # The encounter already printed its own win/lose message.
                self.castle.reset()
                print("\nGame Over")
                if not self.ask_play_again():
                    print("Farewell, adventurer.")
                    break
                print("\nYou enter a new castle...")

    @staticmethod
    def ask_play_again():
        """Return True if the player wants to explore a different castle."""
        while True:
            answer = input("Would you like to explore a different castle? (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please answer 'y' or 'n'.")


# run the game
if __name__ == "__main__":
    try:
        Game(rooms).play_game()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D: exit cleanly instead of showing a traceback
        print("\nYou flee the castle. Goodbye!")
