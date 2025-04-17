import math
import time
import numpy as np 

#game board
initial_state = np.full((3,3)," ")

def print_board(board):
    for row in board:
        print("| " + " | ".join(row) + " |")
    print()

#check if game is over or not
def terminal(state):
    for row in state:
        if row[0] == row[1] == row[2] != " ":
            return True

    for col in range(3):
        if state[0][col] == state[1][col] == state[2][col] != " ":
            return True

    if state[0][0] == state[1][1] == state[2][2] != " ":
        return True
    if state[0][2] == state[1][1] == state[2][0] != " ":
        return True

    if all(cell != " " for row in state for cell in row):
        return True

    return False

#calculate the terminal state value
def utility(state):
    for row in state:
        if row[0] == row[1] == row[2] == "X":
            return 1
        if row[0] == row[1] == row[2] == "O":
            return -1

    for col in range(3):
        if state[0][col] == state[1][col] == state[2][col] == "X":
            return 1
        if state[0][col] == state[1][col] == state[2][col] == "O":
            return -1

    if state[0][0] == state[1][1] == state[2][2] == "X":
        return 1
    if state[0][0] == state[1][1] == state[2][2] == "O":
        return -1
    if state[0][2] == state[1][1] == state[2][0] == "X":
        return 1
    if state[0][2] == state[1][1] == state[2][0] == "O":
        return -1

    return 0

#return list of available moves as (row, col) tuples
def actions(state):
    available = []
    for row in range(3):
        for col in range(3):
            if state[row][col] == " ":
                available.append((row, col))
    return available

#return a new state after applying an action but does not modify the original state
def result(state, action, player):
    row, col = action
    if state[row][col] != " ":
        raise ValueError("Invalid action")

    new_state = state.copy()
    new_state[row][col] = player
    return new_state

def max_value(state, alpha, beta):
    if terminal(state):
        return utility(state)

    v = -math.inf
    for action in actions(state):
        v = max(v,min_value(result(state, action, "X"), alpha, beta))
        if v >= beta:
            return v
        alpha=max(alpha,v)

    return v

def min_value(state, alpha, beta):
    if terminal(state):
        return utility(state)

    v = math.inf
    for action in actions(state):
        v= min(v,max_value(result(state, action, "O"), alpha, beta))
        if v <= alpha:
            return v
        beta=min(beta,v)

    return v

def minimax(state, player):
    best_val = -math.inf if player == "X" else math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf
    
    for action in actions(state):
        if player == "X":
            current_val = min_value(result(state, action, "X"), alpha, beta)
            if current_val > best_val:
                best_val = current_val
                best_move = action
            alpha = max(alpha, best_val)
        else:
            current_val = max_value(result(state, action, "O"), alpha, beta)
            if current_val < best_val:
                best_val = current_val
                best_move = action
            beta = min(beta, best_val)
    
    return best_move

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, state):
        while True:
            try:
                move = input(f"Player {self.letter}'s turn (row,col): ")
                row, col = map(int, move.split(","))
                if (row, col) in actions(state):
                    return (row, col)
                print("Invalid move. Try again.")
            except ValueError:
                print("Please enter in format: row,col")

class AIPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, state):
        time.sleep(1)
        return minimax(state,self.letter)

def play_game(): 
    human = HumanPlayer("X")
    ai = AIPlayer("O")

    current_state = initial_state.copy()
    current_player = human 
    while not terminal(current_state):
        print_board(current_state)
        move = current_player.get_move(current_state)
        current_state = result(current_state, move, current_player.letter)
        current_player = ai if current_player == human else human

    print_board(current_state)
    score = utility(current_state)
    if score == 1:
        print("X wins!")
    elif score == -1:
        print("O wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()