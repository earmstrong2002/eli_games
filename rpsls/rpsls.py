import random as rand
import time

MOVE_LIST = [
            'rock',
            'paper',
            'scissors',
            'lizard',
            'spock'
        ]

class Move:
    def __init__(self, beats, name):
        self.beats = beats
        self.name = name
    def __str__(self):
        return self.name
        
        # Evaluate player move against com move
    def evaluate_victor(self, com_move):
            if com_move in self.beats:
                return 'Player wins!'
            elif com_move == self.name:
                return 'It\'s a draw!'
            else:
                return 'Computer wins!'
        
def get_player_move():
    print("Enter your move: ", end='')
    while True:
        user_input = str(input()).casefold()
        if user_input in MOVE_LIST:
            return user_input
        else:
            print('Invalid move. Try again:', end='')
            
def build_tension():
    for i in range(3):
        print('.', end='')
        time.sleep(1)
    print()
        
def main():
    rock = Move(['scissors', 'lizard'], 'rock')
    paper = Move(['rock', 'spock'], 'paper')
    scissors = Move(['paper', 'lizard'], 'scissors')
    lizard = Move(['paper', 'spock'], 'lizard')
    spock = Move(['scissors', 'rock'], 'spock')
    
    player_wins = 0
    com_wins = 0
    
    while True:  
        
        player_move = get_player_move()
        time.sleep(0.5)
        com_move = rand.choice(MOVE_LIST)
        
        build_tension()
        
        print(f'Computer\'s move: {com_move.capitalize()}')
        time.sleep(0.2)
        
        # Determine victor
        match player_move[1]:
            case 'o': victor = rock.evaluate_victor(com_move)
            case 'a': victor = paper.evaluate_victor(com_move)
            case 'c': victor = scissors.evaluate_victor(com_move)
            case 'i': victor = lizard.evaluate_victor(com_move)
            case 'p': victor = spock.evaluate_victor(com_move)
            case _: print('Error parsing player input')

        # Increment scoreboard
        match victor[0].casefold():
            case 'p': player_wins += 1
            case 'c': com_wins += 1
        
        time.sleep(1)    
        print(f'{victor} Current score: Player: {player_wins}, Computer: {com_wins}')
        time.sleep(1)
        
        # Ask if player would like to play again
        leave = False
        while True:
            print('Play again?')
            match str(input())[0].casefold():
                case 'y': break
                case 'n': 
                    print('Exiting game.')
                    leave = True
                    break
                case _:
                    print('Invalid input. Try again.')
            
        if leave == True:
            break
if __name__ == '__main__':
    main()