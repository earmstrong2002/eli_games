import random as rand

class Move:
    def __init__(self, beats):
        self.beats = beats
        
        # Evaluate player move against com move
    def evaluate_victor(self, com_move):
            if com_move in self.beats:
                return 'Player'
            else:
                return 'Computer'
        
def get_player_move():
    print("Enter your move: ", end='')
    return(str(input()))
        
def main():
    rock = Move(['scissors', 'lizard'])
    paper = Move(['rock', 'spock'])
    scissors = Move(['paper', 'lizard'])
    lizard = Move(['paper', 'spock'])
    spock = Move(['scissors', 'rock'])
    
    player_wins = 0
    com_wins = 0
    
    while True:  
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
        
        # Determine victor
        match player_move[1].casefold():
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
            
        print(f'{victor} wins! Current score: Player: {player_wins}, Computer: {com_wins}')
        
        # Ask if player would like to play again
        print('Play again?')
        match str(input())[0].casefold():
            case 'y': continue
            case 'n': exit()
main()