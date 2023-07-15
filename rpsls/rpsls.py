import random as rand

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
            print("Invalid move. Valid inputs are (not case sensitive):")
            print("'rock', 'paper', 'scissors', 'lizard', spock'")
            print("or type 'quit' to close the program")
            
def com_decide(player_history):
    # build map of best options stored in confidence
    confidence = []
    for move in MOVES:
        play_count = 0
        for i in move.beats:
            # report how many times player has played moves
            # that are beaten by move in parent loop
            play_count += player_history[MOVES[MOVE_KEY.index(i)]]
        confidence.append(play_count)
    for i in range(len(confidence)):
        confidence[i] = confidence[i] ** 2
    # randomly choose an option, weighted by the values in confidence
    return rand.choices(MOVES, weights=confidence, k=1)[0]
        
def pad_string(string, length):
    pad = length - len(string)
    return (string + ' ' * pad)

def intro():
    print("Welcome to R.P.S.L.S! Here are the rules:")
    print('Scissors cuts Paper')
    print('paper covers Rock')
    print('Rock crushes Lizard')
    print('Lizard poisons Spock')
    print('Spock smashes Scissors')
    print('Scissors decapitates Lizard')
    print('Lizard eats Paper')
    print('Paper disproves Spock')
    print('Spock vaporizes Rock')
    print('(and as it always has) Rock crushes Scissors')

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
    
    intro()
    
    while True:  
        com_move = com_decide(player_history)
        
        player_move = get_player_move()
        if player_move == 'quit':
            break
        player_history[player_move] += 1
        
        print(f'Computer\'s move: {com_move}')
        
        victor = player_move.evaluate_victor(com_move)
        
        # Increment scoreboard
        match victor[0].casefold():
            case 'p': player_wins += 1
            case 'c': com_wins += 1    
        
        print(f'{pad_string(victor, 45)} Current score: Player: {player_wins}, Computer: {com_wins}')
        
if __name__ == '__main__':
    main()