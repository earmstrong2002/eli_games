import random as rand
import time
import tkinter as tk
import PIL
import numpy as np

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
        
        # Evaluate player move against com move
    def evaluate_victor(self, com_move):
            if com_move.title in self.beats:
                action = self.actions[self.beats.index(com_move.title)]
                return f'Player wins! {self.title.capitalize()} {action} {com_move.title.capitalize()}.'
            elif str(com_move) == str(self):
                return 'It\'s a draw!'
            else:
                action = com_move.actions[com_move.beats.index(self.title)]
                return f'Computer wins! {com_move.title.capitalize()} {action} {self.title.capitalize()}.'

class Button(tk.Button):
    def __init__(self, title, move):
        self['text'] = title
        #TODO finish me!

class Window(tk.Tk):
    def __init__(self):
        self.title('Play R.P.S.L.S.')
        self.geometry('640x360')
        
        self.rowconfigure(0, weight=1, pad=5)
        self.rowconfigure(1, weight=0, pad=5)
        self.columnconfigure(0, weight=1, pad=5)
        
        self.create_widgets()
    
    def create_widgets():
        lbl_placeholder = tk.Label(
            text='bread and butter'
        )
        lbl_placeholder.grid(
            column=0, row=0,
            sticky='nsew'
        )
        
        # make 5 buttons on the bottom
        for btn in range(5):
            #TODO finish me!
            pass

ROCK = Move(('scissors', 'lizard'), 'rock', ('crushes', 'crushes'))
PAPER = Move(('rock', 'spock'), 'paper', ('covers', 'disproves'))
SCISSORS = Move(('paper', 'lizard'), 'scissors', ('cuts', 'decapitates'))
LIZARD = Move(('paper', 'spock'), 'lizard', ('eats', 'poisons'))
SPOCK = Move(('scissors', 'rock'), 'spock', ('smashes', 'vaporizes'))
            
MOVES = [ROCK, PAPER, SCISSORS, LIZARD, SPOCK]
   
            
def get_player_move():
    print("Enter your move: ", end='')

    while True:
        user_input = str(input()).casefold()
        if user_input in MOVE_KEY:
            return MOVES[MOVE_KEY.index(user_input)]
        elif user_input.startswith('q'):
            print('Exiting game.')
            return 'quit'
        else:
            print('Invalid move. Try again: ', end='')
            
def build_tension():
    for i in range(3):
        print('.', end='')
        time.sleep(SPEED)
    print()
        
def com_decide(player_history):
    # build map of best options stored in confidence
    confidence = []
    for move in MOVES:
        play_count = 0
        for i in move.beats:
            play_count += player_history[MOVES[MOVE_KEY.index(i)]]
        confidence.append(play_count)
    for i in range(len(confidence)):
        confidence[i] = confidence[i] ** 2
    # randomly choose an option, weighted by play quality
    return rand.choices(MOVES, weights=confidence, k=1)[0]
        
def player_decide(): #unused
    confidence = [60, 30, 20, 15, 12]   
    return rand.choices(MOVES, weights=confidence, k=1)[0]

def pad_string(string, length):
    pad = length - len(string)
    return (string + ' ' * pad)



def main():
    #TODO make gui
    
    player_wins = 0
    com_wins = 0
    player_history = {
        ROCK: 1,
        PAPER: 1,
        SCISSORS: 1,
        LIZARD: 1,
        SPOCK: 1,
    }
   
    for i in range(100):  
        com_move = com_decide(player_history)
        
        player_move = get_player_move()
        if player_move == 'quit':
            break
        player_history[player_move] += 1
        time.sleep(SPEED / 2)
        
        build_tension()
        print(f'Computer\'s move: {com_move}')
        time.sleep(SPEED / 5)
        
        victor = player_move.evaluate_victor(com_move)
        
        # Increment scoreboard
        match victor[0].casefold():
            case 'p': player_wins += 1
            case 'c': com_wins += 1
        time.sleep(SPEED)    
        
        print(f'{pad_string(victor, 45)} Current score: Player: {player_wins}, Computer: {com_wins}')
        time.sleep(SPEED)
        
if __name__ == '__main__':
    main()