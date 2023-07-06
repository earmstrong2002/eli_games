import random as rand

class Move:
    def __init__(self, beats):
        self.beats = beats
        
def get_player_move():
    print("Enter your move: ", end='')
    return(str(input()))
        
def main():
    rock = Move(['scissors', 'lizard'])
    paper = Move(['rock', 'spock'])
    scissors = Move(['paper', 'lizard'])
    lizard = Move(['paper', 'spock'])
    spock = Move(['scissors', 'rock'])
    
    move_list = [
        'rock',
        'paper',
        'scissors',
        'lizard',
        'spock'
    ]
    
    player_move = get_player_move()
    com_move = rand.choice(move_list)
    
    print(f'Player move: {player_move}')
    print(f'Computer\'s move: {com_move}')
main()