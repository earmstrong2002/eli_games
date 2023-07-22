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
    - calls configure_root_window with target_gamemode
    - calls start_game with target_gamemode
"""


import random as rand
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
import json
from dataclasses import dataclass, field
import os


HERE = Path(__file__).parent.absolute()  # absolute path of current file


@dataclass
class Move:
    """
    Stores info relavent to Rps operations.
    - title stores move's name as str
    - beats stores dict[Move: str];
        - keys are moves that are beaten by self
        - values are the action that makes self beat the key
        - e.g. rock.beats == {scissors, "crushes"}  # rock crushes scissors
    - texture stores Image object with associated texture
        - note: move textures are to be stored with the following format:
        - directory: textures/relaventgamemode/
        - file name: movetitle.png
        - size: 250x250
    """

    title: str = field(default="<unnamed>", frozen=True)
    beats: dict = field(default_factory=dict)
    texture: Image = None


class Rps:
    """A class that serves as a game engine
    for variants of rock, paper, scissors."""

    def __init__(self, gamemode: dict):
        self.gamemode = gamemode["title"]
        self.alias = gamemode["alias"]
        self.moves = self.initialize_moves(gamemode["moves"])

    def _initialize_moves(self, move_dict: dict) -> list[Move]:
        """Creates and configures Move object for each move in move_list"""
        moves = self._instantiate_moves(move_dict)
        move_key = self._build_move_key(moves)
        # Populate Move object attributes
        moves = self._populate_beats(moves, move_key, move_dict)
        moves = self._populate_textures(moves, move_key)
        return moves

    def _instantiate_moves(self, move_list: dict) -> list[Move]:
        """
        Instantiates Move object for each move in move_list.
        Move objects are "naked" because they have only title. No other data.
        """
        naked_moves = []
        for move in move_list:
            exec(f"{move} = Move(title='{move}')")
            exec(f"naked_moves.append({move})")
        return naked_moves

    def _build_move_key(self, moves: list[Move]) -> dict[str, Move]:
        """Returns dict for locating Move object with given title"""
        move_key = {}
        for move in moves:
            move_key[move.title] = move
        return move_key

    def _populate_beats(
        self, moves: list[Move], move_key: dict[str, Move], move_dict: dict
    ) -> dict[str, Move]:
        """Assigns beats attribute to all moves in move_key."""
        for move in moves:
            beats = {}
            # locate relevant data in move_dict
            unformatted_beats = move_dict[move.title]
            for key in unformatted_beats:
                # locate Move corresponding Move object
                move = move_key[key]
                # add Move object and verb to beats
                beats[move] = unformatted_beats[key]
            move.beats = beats
        return moves

    def _populate_textures(
        self, moves: list[Move], move_key: dict[str, Move]
    ) -> dict[str, Move]:
        """
        Assigns texture attribute to Move objects.
        Note: All textures present in gamemode's texture folder
        will be processed, not necessarily every move
        in the gamemode.
        """
        pths_textures = list(
            Path(HERE / "textures" / self.gamemode).glob("*.png")
        )
        for path in pths_textures:
            # instantiate Image object with path
            img = Image.open(path)
            try:
                # locate corrisponding move
                current_move = move_key[path.stem]
            except KeyError:
                # texture file is either misnamed
                # or does not belong in current gamemode.
                # mark bad file invalid.
                os.rename(path.name, "INVALID__" + str(path.name))
            # assign img to move's texture attribute
            move_index = moves.index(current_move)
            moves[move_index].texture = img
        return moves


class App(tk.Frame):
    """App dynamically generates a GUI based on the gamemode information
    stored in the Rps engine passed App's initializer"""


def make_root(move_config: dict, default_gamemode: str) -> None:
    """Instantiates and configures root window with menu bar."""
    global root
    root = tk.Tk()

    configure_root_window(move_config, default_gamemode)
    make_menu_bar(move_config["gamemodes"])


def make_menu_bar(gamemodes: str) -> None:
    """Creates menu bar slaved to root."""
    menu_bar = tk.Menu(root)
    mnu_options = tk.Menu(menu_bar, tearoff=0)
    mnu_gamemodes = make_mnu_gamemodes(mnu_options, gamemodes)

    mnu_options.add_cascade(label="Select Gamemode", menu=mnu_gamemodes)
    menu_bar.add_cascade(label="Options", menu=mnu_options)
    root.config(menu=menu_bar)


def make_mnu_gamemodes(master, gamemodes: list) -> tk.Menu:
    """
    Creates tkinter menu for switching gamemodes.
    The returned menu has one command per gamemode in gamemodes;
    each command calls change_gammeode and passes it
    the appropriate gamemode.
    """
    mnu_gamemodes = tk.Menu(master, tearoff=0)
    for gamemode in gamemodes.items():
        mnu_gamemodes.add_command(
            label=gamemode[1]["alias"],
            command=lambda: change_gamemode(gamemode),
        )
    return mnu_gamemodes


def configure_root_window(move_config, gamemode) -> None:
    """Configures geometry, title, and icon of root window."""
    root.geometry("640x480")
    active_gamemode_alias = move_config["gamemodes"][gamemode]["alias"]
    root.title(f"Play {active_gamemode_alias}")
    with Image.open(HERE / "icon.png") as open_img:
        open_img.resize((16, 16))
        icon = ImageTk.PhotoImage(open_img)
    root.wm_iconphoto(True, icon)


def start_game(gamemode: str) -> None:
    """Instantiates Rps engine and App frame with given gamemode."""
    rps = Rps(gamemode)
    app = App(rps)


def instantiate_rps(gamemode: str) -> Rps:
    """Creates an instance of Rps with the given gamemode."""


def instantiate_app(engine: Rps) -> App:
    """Creates instance of Rps with the given Rps engine."""


def change_gamemode(gamemode: str) -> None:
    """
    Changes gamemode by destroying currently active instances of
    Rps and App and reinstantiating them with the given gamemode.
    """


def main():
    with open(HERE / "move_config.json") as cfg:
        move_config = json.load(cfg)  # config dict
    default_gamemode = move_config["default_gamemode"]
    make_root(move_config, default_gamemode)
    start_game(default_gamemode)
    root.mainloop()


if __name__ == "__main__":
    main()
