# bccm2
 The Broken Shield HexDNA Character Manager Version 2 

## Requirements
- Python 3.10+
- Poetry
- Pydantic
- Rest of requirements can be found in `pyproject.toml`

## Developed by 
Gunnar Roxen gunnar@brokenshield.net

## License
TBD - currently copyright (c) Gobion Rowlands

## Installation and Operation
1. First ensure you have Python 3.10+ installed
2. Install Poetry: [https://python-poetry.org/docs/]
3. Change to directory you cloned the git repo to and type:
```$ poetry install```
4. This will install all the python modules required. It might take a few moments.
5. Enter the Poetry virtual environment shell with:
```$ poetry shell```
6. Then run the main python script:
```$ python main.py```
7. To exit the poetry shell, simply type:
```$ exit```

## Terminology
- **Player**: A player (real world person) of Broken Shield
- **Character**: A map of nodes and mod_ids with supplemental info that forms a character. Each character is tied to a specific `player_id`.
- **LiveCharacter**: A dynamic summary of the character which is where you find all the actual stats. Each live character is tied to a specific `char_id`.
- **Node** = character sheet location (e.g. breed_n0, physical_n0, physical_opportunity_n0)
- **Mod_id** = Things characters get, edges, traits, skills, opportunities, sliverware, echo powers, gifts etc. (e.g. e_brave, s_cnsbooster, l_lifestyle_downtown)
- **Stat** = live calculated element based on mod_ids (e.g. physical = 6, athletics = 2,)

## Key Files
- `main.py`: the main python script for BSCM2. Start here
- `run_gamedata_export.py`: exports the contents of `./gamedata/broken_shield_gamedata.xlsx` to same named SQLite3 DB and JSON file
- `character_dataclasses.py`: pydantic validated set of dataclasses used in the 
- `cli_methods.py`: Command Line Interface front end for BSCM2
- `test_character_methods.py`: suite of tests for character_methods.py, delete_methods.py and utility_methods.py
bccm2
- `delete_methods.py`: the only methods that allow deletion and purging of players, characters and live_characters (`extends character_methods.py`)
- `character_methods.py`: core functionality of bccm2 (`extends utility_methods.py`)
- `utility_methods.py`: a set of general purpose utility methods for bccm2
- `./gamedata/broken_shield_gamedata.sqlite`: SQLite3 DB of all game data
- `./characters/broken_shield_characters.sqlite`: SQLite3 DB of all characters
- Gamedata is also saved as `broken_shield_gamedata.json` for review purposes.