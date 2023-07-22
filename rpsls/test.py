import json
from pathlib import Path

HERE = Path(__file__).parent.absolute()  # absolute path of current file

with open(HERE / "move_config.json") as cfg:
    move_config = json.load(cfg)

for move in move_config["gamemodes"]["rpsls"]["moves"].items():
    print(move)
