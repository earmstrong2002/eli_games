import random as rand
import time
import tkinter
import PIL
import numpy as np

SPEED = 0.1

class Move:
    def __init__(self, beats, title, actions):
        self.beats = beats
        self.title = title
        self.actions = actions
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

ROCK = Move(('scissors', 'lizard'), 'rock', ('crushes', 'crushes'))
PAPER = Move(('rock', 'spock'), 'paper', ('covers', 'disproves'))
SCISSORS = Move(('paper', 'lizard'), 'scissors', ('cuts', 'decapitates'))
LIZARD = Move(('paper', 'spock'), 'lizard', ('eats', 'poisons'))
SPOCK = Move(('scissors', 'rock'), 'spock', ('smashes', 'vaporizes'))
            
MOVES = [ROCK, PAPER, SCISSORS, LIZARD, SPOCK]
   
MOVE_KEY = [
'rock',
'paper',
'scissors',
'lizard',
'spock'
]
            
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
        
def com_decide(player_history): #FIXME
    # sort dict of player_history by frequency
    dist = dict(reversed(sorted(player_history.items(),
                                key=lambda item: item[1])))
    top_moves = list(dist.items())
    best_option = rand.choice(MOVES)
    if top_moves[0][1] > 0:
        top_move = top_moves[0][0].title
        # find what beats player's most used move
        beats_top = []
        for move in MOVES:
            if top_move in move.beats:
                beats_top.append(move.title)
        best_option = MOVES[MOVE_KEY.index(rand.choice(beats_top))]
        # find what beats the options that beat player's top move
        threats = [] # temp storage for the moves that beat each option
        beaten_by = [] # moves that beat each option
        for option in beats_top:
            for move in MOVES:
                if option in move.beats:
                    threats.append(move.title)
            if len(threats) > 1:
                beaten_by.append(tuple(threats))
            threats.clear()
        # find which option is beaten by less frequently used player moves
        better_move = []
        best_option_beaten_freq = 0.5
        for option in beaten_by:
            option_beaten_freq = 0
            for i in option:
                for move in top_moves:
                    if move[0].title == i:
                        option_beaten_freq += move[1]
                if option_beaten_freq != 0:
                    if (np.reciprocal(option_beaten_freq)
                            <= np.reciprocal(best_option_beaten_freq)):
                        best_option_beaten_freq = option_beaten_freq
                        best_option = (MOVES[MOVE_KEY.index(beats_top
                                      [beaten_by.index(option)])])
                        
    print(f'chose {best_option}')
    # return MOVES[MOVE_KEY.index(best_option)]
    return best_option
        
def main():
    #TODO make gui
    
    player_wins = 0
    com_wins = 0
    player_history = {
        ROCK: 0,
        PAPER: 0,
        SCISSORS: 0,
        LIZARD: 0,
        SPOCK: 0
    }
    
    while True:  
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
        
        print(f'{victor} Current score: Player: {player_wins}, Computer: {com_wins}')
        time.sleep(SPEED)
        
if __name__ == '__main__':
    main()