import random as rand
import tkinter as tk
from tkinter import ttk

SPEED = 1

MOVE_KEY = [
'rock',
'paper',
'scissors',
'lizard',
'spock'
]

class Move:
    def __init__(self, beats, title, actions):
        self.beats = beats
        self.beaten_by = []
        self.title = title
        self.actions = actions
        for move in MOVE_KEY:
            if move not in self.beats and move != self.title:
                self.beaten_by.append(move)
                
    def __str__(self):
        return self.title

ROCK = Move(('scissors', 'lizard'), 'rock', ('crushes', 'crushes'))
PAPER = Move(('rock', 'spock'), 'paper', ('covers', 'disproves'))
SCISSORS = Move(('paper', 'lizard'), 'scissors', ('cuts', 'decapitates'))
LIZARD = Move(('paper', 'spock'), 'lizard', ('eats', 'poisons'))
SPOCK = Move(('scissors', 'rock'), 'spock', ('smashes', 'vaporizes'))
            
MOVES = [ROCK, PAPER, SCISSORS, LIZARD, SPOCK]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x360')
        self.title('Play R.P.S.L.S.')
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
        self.frm_display = ttk.Frame(self.frm_main, relief='groove', border=10)
        self.frm_display.columnconfigure((0, 1, 2), weight=1, pad=5)
        self.frm_display.rowconfigure((0, 1), weight=1, pad=5)
        self.frm_display.grid(column=0, row=0, sticky='nsew',)
        
        # populate display        
        self.lbl_scoreboard = ttk.Label(
            self.frm_display,
            text=f'Player wins: 0, Com wins: 0'
        )
        self.lbl_scoreboard.grid(column = 1, row=0)
        
    def increment_scoreboard(self):
        self.lbl_scoreboard['text'] = f'Player wins: {rps.player_wins}, Com wins: {rps.com_wins}'
        
    def make_move_picker(self):
        # configure frame for move picker
        self.frm_move_picker = ttk.Frame(self.frm_main)
        self.frm_move_picker.rowconfigure(0, weight=1, pad=5)
        self.frm_move_picker.columnconfigure((0, 1, 2, 3, 4), weight=1, pad=5)
        self.frm_move_picker.grid(column=0, row=1, sticky='nsew')
        
        # populate move picker
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
        self.com_wins = 0

    def com_decide(self):
        # build map of best options stored in confidence
        confidence = []
        for move in MOVES:
            play_count = 0
            for i in move.beats:
                play_count += self.player_history[MOVES[MOVE_KEY.index(i)]]
            confidence.append(play_count)
        for i in range(len(confidence)):
            confidence[i] = confidence[i] ** 2
        # randomly choose an option, weighted by play quality
        return rand.choices(MOVES, weights=confidence, k=1)[0]

    def evaluate_victor(self, player_move, com_move):
        if com_move.title == player_move.title:
            action = None
            victor = 'draw'
        elif com_move.title in player_move.beats:
            action = (player_move.actions
                        [player_move.beats.index(com_move.title)])
            victor = 'player'
        else: # computer wins
            action = com_move.actions[com_move.beats.index(player_move.title)]
            victor = 'com'
        return (victor, action)
    
    def increment_scoreboard(self, player_move, victor):
        self.player_history[player_move] += 1
        match victor[0][0]:
            case 'p': self.player_wins += 1
            case 'c': self.com_wins += 1

def run_game(player_move):
    print(player_move)
    com_move = rps.com_decide()
    print(com_move)
    victor = rps.evaluate_victor(player_move, com_move)
    print(victor)
    rps.increment_scoreboard(player_move, victor)
    root.increment_scoreboard()
    
def main():
    global rps
    global root
    rps = Rps()
    root = App()
    root.mainloop()
     
if __name__ == '__main__':
    main()