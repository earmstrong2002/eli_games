import random as rand
import tkinter as tk
from tkinter import ttk
from PIL import Image
from pathlib import Path
from sys import platform

class Move:
    def __init__(self, title, beats=None, actions=None, texture=None):
        self.beats = beats
        self.title = title
        self.actions = actions
        self.texture = texture
                
    def __str__(self):
        return self.title

# instantiates Move objects
def initialize_moves(): 
    global ROCK
    global PAPER
    global SCISSORS
    global LIZARD
    global SPOCK
    global MOVES
    
    ROCK = Move('rock')
    PAPER = Move('paper')
    SCISSORS = Move('scissors')
    LIZARD = Move('lizard')
    SPOCK = Move('spock')
    
    # list for iterating through all moves
    MOVES = [ROCK, PAPER, SCISSORS, LIZARD, SPOCK]
    
    # defining which moves each move beats
    ROCK.beats = (SCISSORS, LIZARD)
    PAPER.beats = (ROCK, SPOCK)
    SCISSORS.beats = (PAPER, LIZARD)
    LIZARD.beats = (PAPER, SPOCK)
    SPOCK.beats = (ROCK, SCISSORS)
    
    # defining what verb to use when each move beats each other move
    ROCK.actions = ('crushes', 'crushes')
    PAPER.actions = ('covers', 'disproves')
    SCISSORS.actions = ('cuts', 'decapitates')
    LIZARD.actions = ('eats', 'poisons')
    SPOCK.actions = ('vaporizes', 'smashes')
    
    # getting file directories for associated move textures
    pths_textures = list(Path('rpsls/textures/').glob('*'))
    strs_textures = []
    for pth in pths_textures: # convert path objects to strings for processing
        strs_textures.append(str(pth))
    if platform.startswith('win'): # replace \ with / for compatability
        for i in range(len(strs_textures)):
            strs_textures[i] = strs_textures[i].replace('\\', '/')
            
    filenames_textures = []
    for pth in strs_textures: # isolate file name, without extension
        im_name = pth.split('/')[-1][:-4]
        filenames_textures.append(im_name)
    
    for move in MOVES: # assign textures to appropriate move objects
        index = filenames_textures.index(move.title)
        move.texture = Image.open(pths_textures[index])

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x360')
        self.title('Play R.P.S.L.S.')
        self.resizable(0, 0) # not resizeable, for simplicity
        #TODO FINALIZE LAYOUT
        #TODO incorporate ttk styles
        #TODO add GRAPHICS
        self.make_widgets()
    
    def make_widgets(self):
        # configure primary frame
        self.frm_main = ttk.Frame(self)
        self.frm_main.columnconfigure(0, weight=1)
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.rowconfigure(1, weight=0, minsize=60)
        self.frm_main.pack(fill='both', expand=True)
        
        # populate with elements
        self.make_display()
        self.make_move_picker()
        
        # establish ttk theme
        self.default = ttk.Style()
        self.default.theme_settings('default', { #FIXME style is not applied to widgets
            'TButton': {
                'map': {
                    'foreground': [('pressed', 'thistle4'),
                                    ('active', 'thistle1')]
                }
            }
        })
        
    def make_display(self):
        # configure frame for display
        self.frm_display = ttk.Frame(self.frm_main)
        self.frm_display.columnconfigure((0, 1, 2), weight=1, pad=5)
        self.frm_display.rowconfigure(0, weight=0, minsize=50, pad=5)
        self.frm_display.rowconfigure(1, weight=1, pad=5)
        self.frm_display.grid(column=0, row=0, sticky='nsew',)
        
        # scoreboard       
        self.scoreboard = tk.StringVar(
            value=f'{rps.player_wins} -- {rps.draws} -- {rps.com_wins}'
            )
        self.lbl_scoreboard = ttk.Label(
            self.frm_display,
            textvariable=self.scoreboard
            )
        self.lbl_scoreboard.grid(column = 1, row=0)
        
        # player label
        self.lbl_player = ttk.Label(self.frm_display, text='Player')
        self.lbl_player.grid(column=0, row=0, sticky='e')
        
        # computer label
        self.lbl_com = ttk.Label(self.frm_display, text='Computer')
        self.lbl_com.grid(column=2, row=0, sticky='w')
        
        self.make_screen()
        
    def make_screen(self):
        pass
    
    def increment_scoreboard(self):
        self.scoreboard.set(
            f'{rps.player_wins} -- {rps.draws} -- {rps.com_wins}'
            )
        
    def make_move_picker(self):
        # configure frame for move picker
        self.frm_move_picker = ttk.LabelFrame(
            self.frm_main,
            text='Pick Your Move',
            labelanchor='n'
            )
        self.frm_move_picker.rowconfigure(0, weight=1, pad=5)
        self.frm_move_picker.columnconfigure((0, 1, 2, 3, 4), weight=1, pad=5)
        self.frm_move_picker.grid(column=0, row=1, sticky='nsew')
        
        # populate move picker
        #TODO make move button constructor modular
        btn_rock = ttk.Button(self.frm_move_picker, text='ROCK',
                             command=lambda: run_game(ROCK))
        btn_rock.grid(column=0, row=0, sticky='nsew')
        btn_paper = ttk.Button(self.frm_move_picker, text='PAPER',
                              command=lambda: run_game(PAPER))
        btn_paper.grid(column=1, row=0, sticky='nsew')
        btn_scissors = ttk.Button(self.frm_move_picker, text='SCISSORS',
                              command=lambda: run_game(SCISSORS))
        btn_scissors.grid(column=2, row=0, sticky='nsew')
        btn_lizard = ttk.Button(self.frm_move_picker, text='LIZARD',
                              command=lambda: run_game(LIZARD))
        btn_lizard.grid(column=3, row=0, sticky='nsew')
        btn_spock = ttk.Button(self.frm_move_picker, text='SPOCK',
                              command=lambda: run_game(SPOCK))
        btn_spock.grid(column=4, row=0, sticky='nsew')
        
class Rps():
    def __init__(self):
        self.player_history = {
            ROCK: 1,
            PAPER: 1,
            SCISSORS: 1,
            LIZARD: 1,
            SPOCK: 1,

        }
        self.player_wins = 0
        self.draws = 0
        self.com_wins = 0

    def com_decide(self):
        # build map of best options stored in confidence
        confidence = []
        for move in MOVES:
            play_count = 0
            for i in move.beats:
                play_count += self.player_history[i]
            confidence.append(play_count)
        for i in range(len(confidence)):
            confidence[i] = confidence[i] ** 2
        # randomly choose an option, weighted by play quality
        return rand.choices(MOVES, weights=confidence, k=1)[0]

    def evaluate_victor(self, player_move, com_move):
        if com_move == player_move:
            action = None
            victor = 'draw'
        elif com_move in player_move.beats:
            action = (player_move.actions
                        [player_move.beats.index(com_move)])
            victor = 'player'
        else: # computer wins
            action = com_move.actions[com_move.beats.index(player_move)]
            victor = 'com'
        return (victor, action)
    
    def increment_scoreboard(self, player_move, victor):
        self.player_history[player_move] += 1
        match victor[0][0]:
            case 'p': self.player_wins += 1
            case 'c': self.com_wins += 1
            case 'd': self.draws += 1

def run_game(player_move):
    print(player_move)
    com_move = rps.com_decide()
    print(com_move)
    victor = rps.evaluate_victor(player_move, com_move)
    print(victor)
    rps.increment_scoreboard(player_move, victor)
    root.increment_scoreboard()
    
def main():
    initialize_moves()
    global rps
    global root
    rps = Rps()
    root = App()
    root.mainloop()
     
if __name__ == '__main__':
    main()