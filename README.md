# Python Text Games with Claude Code

Adapted from the Coursera guided project "GitHub Copilot with Python: Creating Text Games",
built with Claude Code instead of Copilot.

| File | What it is |
|---|---|
| `rpsls.py` | Rock Paper Scissors Lizard Spock: number or name input, play-again loop |
| `rpsls_initial.py` | First-pass RPSLS, kept for before/after comparison |
| `Practice/rps.py` | Practice: classic Rock Paper Scissors |
| `adv_game.py` | Castle text adventure: random rooms, Red and Blue Wizard spell battles, find the treasure to win |

Run any of them with Python 3 (standard library only):

```bash
python3 adv_game.py
```

## Extending the adventure

- New encounter: subclass `Encounter`, implement `run_encounter()` returning an
  `EncounterOutcome`, and add a `Room` using it to the `rooms` list.
- New wizard: subclass `SpellBattleEncounter` and set `wizard_name`,
  `game_rules` and `win_verbs`.
