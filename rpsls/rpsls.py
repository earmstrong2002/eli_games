import random as rand
import time
import tkinter
import PIL

SPEED = 0.1

class Move:
    def __init__(self, beats, title):
        self.beats = beats
        self.title = title
    def __str__(self):
        return self.title
        
        # Evaluate player move against com move
    def evaluate_victor(self, com_move):
            if str(com_move) in self.beats:
                return 'Player wins!'
            elif str(com_move) == str(self):
                return 'It\'s a draw!'
            else:
                return 'Computer wins!'

ROCK = Move(['scissors', 'lizard'], 'rock')
PAPER = Move(['rock', 'spock'], 'paper')
SCISSORS = Move(['paper', 'lizard'], 'scissors')
LIZARD = Move(['paper', 'spock'], 'lizard')
SPOCK = Move(['scissors', 'rock'], 'spock')
            
MOVES = [ROCK, PAPER, SCISSORS, LIZARD, SPOCK]
        
def get_player_move():
    print("Enter your move: ", end='')
    move_key = [
        'rock',
        'paper',
        'scissors',
        'lizard',
        'spock'
    ]
    while True:
        user_input = str(input()).casefold()
        if user_input in move_key:
            return MOVES[move_key.index(user_input)]
        elif user_input.startswith('q'):
            print('Exiting game.')
            return 'quit'
        else:
            print('Invalid move. Try again:', end='')
            
def build_tension():
    for i in range(3):
        print('.', end='')
        time.sleep(SPEED)
    print()
        
def com_decide(player_history):
    #TODO make ai
    dist = dict(reversed(sorted(player_history.items(),
                                key=lambda item: item[1])))     

def main():
    #TODO make gui
    #TODO add unique result messages
    
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
        com_decide(player_history)
        com_move = rand.choice(MOVES)
        
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