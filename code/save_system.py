import json
import os

SAVE_FILE = "savefile.json"

def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "coins": 0,
            "inventory": [],
            "max_energy": 100
        }
