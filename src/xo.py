import tictactoe_solver as t

def display_board(board):
    """Display the board in a 3x3 grid"""
    symbols = {0: '.', 1: 'X', 2: 'O'}
    print()
    for i in range(3):
        row = board[i*3:(i+1)*3]
        print('  ' + ' | '.join(symbols[cell] for cell in row))
        if i < 2:
            print('  ' + '-'*9)
    print()

def display_scores(scores, board):
    """Display scores in a 3x3 grid, showing only valid moves"""
    print("  Scores for each move:")
    print()
    for i in range(3):
        row_scores = scores[i*3:(i+1)*3]
        row_board = board[i*3:(i+1)*3]
        display = []
        for j, (score, cell) in enumerate(zip(row_scores, row_board)):
            if cell == 0:  # empty cell
                display.append(f"{score:>4}")
            else:
                display.append("   .")
        print('  ' + ' | '.join(display))
        if i < 2:
            print('  ' + '-'*14)
    print()

def play_game(misere=False):
    """Interactive game where you play both sides"""
    board = [0] * 9
    mode_name = "Misère" if misere else "Normal"
    print(f"\n=== {mode_name} Tic-Tac-Toe ===")
    print("Play both sides! X goes first, then O")
    print("Positions are 0-8 (top-left to bottom-right)")
    
    display_board(board)
    
    while True:
        # Calculate and show scores
        scores = t.solve(board, misere)
        
        # Determine current player
        num_moves = sum(1 for x in board if x != 0)
        current_player = 1 if num_moves % 2 == 0 else 2
        player_symbol = 'X' if current_player == 1 else 'O'
        
        print(f"\n{player_symbol}'s turn (Player {current_player})")
        display_scores(scores, board)
        
        # Check if game is over
        pos = Position(board)
        result = pos.concluded()
        if result != -1:
            if result == 0:
                print("Game Over: Draw!")
            elif result == 1:
                print("Game Over: X wins!" if not misere else "Game Over: X loses (O wins)!")
            else:
                print("Game Over: O wins!" if not misere else "Game Over: O loses (X wins)!")
            break
        
        # Get player move
        while True:
            try:
                move = int(input(f"{player_symbol}'s move (0-8): "))
                if 0 <= move <= 8 and board[move] == 0:
                    break
                print("Invalid move! Choose an empty position.")
            except (ValueError, KeyboardInterrupt):
                print("\nExiting...")
                return
        
        # Make move
        board[move] = current_player
        display_board(board)

class Position:
    """Python mirror of C++ Position struct for checking game state"""
    def __init__(self, board):
        self.board = board
    
    def concluded(self):
        b = self.board
        # rows
        if b[0] and b[0] == b[1] == b[2]: return b[0]
        if b[3] and b[3] == b[4] == b[5]: return b[3]
        if b[6] and b[6] == b[7] == b[8]: return b[6]
        # columns
        if b[0] and b[0] == b[3] == b[6]: return b[0]
        if b[1] and b[1] == b[4] == b[7]: return b[1]
        if b[2] and b[2] == b[5] == b[8]: return b[2]
        # diagonals
        if b[0] and b[0] == b[4] == b[8]: return b[0]
        if b[2] and b[2] == b[4] == b[6]: return b[2]
        # draw
        if all(b): return 0
        return -1

if __name__ == "__main__":
    print("1. Normal Tic-Tac-Toe")
    print("2. Misère Tic-Tac-Toe")
    choice = input("Choose mode (1 or 2): ")
    
    misere = choice == "2"
    play_game(misere)
