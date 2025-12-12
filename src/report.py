import tictactoe_solver as t
import xo

# ========================================
# 1. OPENING MOVE ANALYSIS
# ========================================
print("=" * 50)
print("OPENING MOVE ANALYSIS")
print("=" * 50)

print("\n--- Normal Tic-Tac-Toe ---")
scores_normal = t.solve([0] * 9, False)
print("Empty board scores:", scores_normal)
print("Interpretation: All moves lead to draws with perfect play")

print("\n--- Misère Tic-Tac-Toe ---")
scores_misere = t.solve([0] * 9, True)
print("Empty board scores:", scores_misere)
print("Best opening move(s):", [i for i, s in enumerate(scores_misere) if s == max(scores_misere)])
print("Interpretation: Only center (position 4) leads to a draw!")

# ========================================
# 2. SYMMETRY VERIFICATION
# ========================================
print("\n" + "=" * 50)
print("SYMMETRY VERIFICATION")
print("=" * 50)

# Corner equivalence
print("\nCorner positions (0, 2, 6, 8):")
corners = [0, 2, 6, 8]
print("Normal:", [scores_normal[i] for i in corners])
print("Misère:", [scores_misere[i] for i in corners])

# Edge equivalence
print("\nEdge positions (1, 3, 5, 7):")
edges = [1, 3, 5, 7]
print("Normal:", [scores_normal[i] for i in edges])
print("Misère:", [scores_misere[i] for i in edges])

# Center
print("\nCenter position (4):")
print("Normal:", scores_normal[4])
print("Misère:", scores_misere[4])

# ========================================
# 3. MID-GAME POSITION ANALYSIS
# ========================================
print("\n" + "=" * 50)
print("MID-GAME POSITION ANALYSIS")
print("=" * 50)

# Position where X can win immediately
print("\nPosition: X can win (should show high score at position 2)")
print("Board: X X _ | O O _ | _ _ _")
board1 = [1, 1, 0, 2, 2, 0, 0, 0, 0]
scores1 = t.solve(board1, False)
print("Scores:", scores1)
print("Best move:", scores1.index(max([s for s in scores1 if s != -999999])))

# Position where O must block
print("\nPosition: O must block (should show defensive move)")
print("Board: X X _ | O _ _ | _ _ _")
board2 = [1, 1, 0, 2, 0, 0, 0, 0, 0]
scores2 = t.solve(board2, False)
print("Scores:", scores2)
print("O's best move:", scores2.index(max([s for s in scores2 if s != -999999])))

# Fork position
print("\nPosition: X creates a fork")
print("Board: X _ _ | _ X _ | _ _ O")
board3 = [1, 0, 0, 0, 1, 0, 0, 0, 2]
scores3 = t.solve(board3, False)
print("Scores:", scores3)
print("Best moves for X:", [i for i, s in enumerate(scores3) if s == max([x for x in scores3 if x != -999999])])

# ========================================
# 4. MISÈRE MODE TACTICAL DIFFERENCES
# ========================================
print("\n" + "=" * 50)
print("MISÈRE MODE TACTICAL DIFFERENCES")
print("=" * 50)

print("\nSame position evaluated in both modes:")
print("Board: X _ _ | _ O _ | _ _ _")
board4 = [1, 0, 0, 0, 2, 0, 0, 0, 0]
scores_normal_mid = t.solve(board4, False)
scores_misere_mid = t.solve(board4, True)
print("Normal scores:", scores_normal_mid)
print("Misère scores:", scores_misere_mid)
print("\nNote how optimal moves differ between modes!")

# ========================================
# 5. GAME STATE STATISTICS
# ========================================
print("\n" + "=" * 50)
print("GAME COMPLEXITY METRICS")
print("=" * 50)

print("\nTic-Tac-Toe State Space:")
print("- Total possible board states: 3^9 = 19,683")
print("- Legal positions (after symmetry): ~5,478")
print("- Game tree complexity: ~255,168 nodes")
print("- Maximum game length: 9 moves")
print("\nYour solver uses:")
print("- Minimax with alpha-beta pruning")
print("- Base-3 position encoding for efficient representation")
print("- Depth-dependent scoring (faster wins preferred)")

# ========================================
# 6. PERFORMANCE TEST
# ========================================
print("\n" + "=" * 50)
print("PERFORMANCE TEST")
print("=" * 50)

import time

# Test solving from empty board
start = time.time()
for _ in range(100):
    t.solve([0] * 9, False)
end = time.time()
print(f"\nSolving empty board 100 times: {(end-start)*1000:.2f}ms total")
print(f"Average time per solve: {(end-start)*10:.3f}ms")

# Test solving from mid-game
start = time.time()
for _ in range(100):
    t.solve([1, 1, 0, 2, 2, 0, 0, 0, 0], False)
end = time.time()
print(f"\nSolving mid-game position 100 times: {(end-start)*1000:.2f}ms total")
print(f"Average time per solve: {(end-start)*10:.3f}ms")

# ========================================
# 7. EXAMPLE PERFECT GAME
# ========================================
print("\n" + "=" * 50)
print("PERFECT GAME SIMULATION")
print("=" * 50)

print("\nSimulating a game where both players play optimally:")
game_board = [0] * 9
move_num = 1

while True:
    pos = xo.Position(game_board)
    if pos.concluded() != -1:
        break
    
    scores = t.solve(game_board, False)
    best_score = max([s for s in scores if s != -999999])
    best_moves = [i for i, s in enumerate(scores) if s == best_score]
    move = best_moves[0]  # Take first optimal move
    
    player = 1 if sum(1 for x in game_board if x != 0) % 2 == 0 else 2
    game_board[move] = player
    
    print(f"\nMove {move_num}: Player {player} plays position {move}")
    print(f"Score: {best_score}")
    xo.display_board(game_board)
    move_num += 1

result = xo.Position(game_board).concluded()
if result == 0:
    print("Result: Draw (as expected with perfect play!)")
elif result == 1:
    print("Result: X wins")
else:
    print("Result: O wins")

print("\n" + "=" * 50)
print("Analysis complete!")
print("=" * 50)
