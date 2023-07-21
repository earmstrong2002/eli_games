"""
Intended Structure:
- main
    - loads move_config.json
    - calls helper function to create root window with gamemodes
    - calls start_game with default gamemode
        - calls helper function to instantiate global Rps with default gamemode
        - instantiates global App, which inherits from Rps and makes frame
            slaved to root
    - initiates root.mainloop()
    
- change_gamemode
    - accepts target_gamemode,
    - kills existing Rps and App
    - calls start_game with target_gamemode
"""


import random as rand
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
import json


HERE = Path(__file__).parent.absolute()


class Move:
    """Dataclass storing info relavent to Rps operations
    - self.title stores move's name as str
    - self.beats stores dict[Move: str];
        - keys are moves that are beaten by self
        - values are the action that makes self beat the key
        - e.g. rock.beats == {scissors, "crushes"}  # rock crushes scissors
    - self.texture stores Image object with associated texture
        - note: move textures are to be stored with the following format:
        - directory: textures/relaventgamemode/
        - file name: movetitle.png
        - size: 250x250
    """

    def __init__(self, title: str, beats: dict = None, texture: Image = None):
        self.title = title
        self.beats = beats
        self.texture = texture

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        repr = "Move; title={}, beats={}, texture={}"
        return repr.format(str(self.title), str(self.beats), str(self.texture))


def make_root(move_config) -> tk.Tk:
    root = tk.Tk()
    # configure root window
    root.geometry("640x480")
    title = f"Play {move_config['default_gamemode']}"
    root.title(title)
    with open(HERE / "icon.png") as open_img:
        open_img.resize((16, 16))
        icon = ImageTk.PhotoImage(icon)
    root.wm_iconphoto(True, icon)

    # create menu bar
    menu_bar = tk.Menu(root)
    mnu_options = tk.Menu(menu_bar)

    menu_bar.addcascade(mnu_options)
    root.config(menu=menu_bar)


def start_game(gamemode: str) -> None:
    instantiate_rps(gamemode)
    instantiate_App(gamemode)


def main():
    with open(cfg_pth / "move_config.json") as cfg:
        move_config = json.load(cfg)
    root = make_root(move_config)


if __name__ == "__main__":
    main()
