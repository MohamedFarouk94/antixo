import tkinter as tk
from tkinter import font as tkfont
import xo
import tictactoe_solver as t

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XO Game")
        self.root.configure(bg='#1a1a2e')
        
        # Game state
        self.board = [0] * 9
        self.misere = False
        self.game_over = False
        self.winning_line = None
        
        # Colors
        self.bg_color = '#16213e'
        self.grid_color = '#0f3460'
        self.x_color = '#4a90e2'
        self.o_color = '#f4a261'
        self.positive_color = '#4a90e2'
        self.negative_color = '#f4a261'
        self.neutral_color = '#9b59b6'
        self.win_highlight = '#27ae60'
        self.lose_highlight = '#e74c3c'
        
        # Fonts
        self.symbol_font = tkfont.Font(family='Helvetica', size=48, weight='bold')
        self.score_font = tkfont.Font(family='Helvetica', size=14)
        self.hover_font = tkfont.Font(family='Helvetica', size=48, weight='bold')
        
        # Create UI
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        # Top frame for controls
        top_frame = tk.Frame(self.root, bg='#1a1a2e', pady=10)
        top_frame.pack()
        
        # Misere toggle
        self.misere_var = tk.BooleanVar(value=False)
        toggle_btn = tk.Checkbutton(
            top_frame,
            text="Misère Mode",
            variable=self.misere_var,
            command=self.toggle_misere,
            bg='#1a1a2e',
            fg='#ffffff',
            selectcolor='#0f3460',
            font=('Helvetica', 12),
            activebackground='#1a1a2e',
            activeforeground='#ffffff',
            bd=0,
            highlightthickness=0
        )
        toggle_btn.pack(side=tk.LEFT, padx=10)
        
        # Reset button
        reset_btn = tk.Button(
            top_frame,
            text="New Game",
            command=self.reset_game,
            bg='#0f3460',
            fg='#ffffff',
            font=('Helvetica', 12),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        # Game frame
        game_frame = tk.Frame(self.root, bg='#1a1a2e')
        game_frame.pack(pady=20)
        
        # Create 3x3 grid of cells
        self.cells = []
        for i in range(9):
            cell = tk.Canvas(
                game_frame,
                width=120,
                height=120,
                bg=self.bg_color,
                highlightthickness=2,
                highlightbackground=self.grid_color,
                cursor='hand2'
            )
            cell.grid(row=i//3, column=i%3, padx=2, pady=2)
            cell.bind('<Button-1>', lambda e, idx=i: self.make_move(idx))
            cell.bind('<Enter>', lambda e, idx=i: self.on_hover(idx))
            cell.bind('<Leave>', lambda e, idx=i: self.on_leave(idx))
            self.cells.append(cell)
    
    def toggle_misere(self):
        self.misere = self.misere_var.get()
        if not self.game_over:
            self.update_display()
    
    def reset_game(self):
        self.board = [0] * 9
        self.game_over = False
        self.winning_line = None
        self.update_display()
    
    def get_current_player(self):
        num_moves = sum(1 for x in self.board if x != 0)
        return 1 if num_moves % 2 == 0 else 2
    
    def make_move(self, idx):
        if self.board[idx] == 0 and not self.game_over:
            self.board[idx] = self.get_current_player()
            self.check_game_over()
            self.update_display()
    
    def check_game_over(self):
        pos = xo.Position(self.board)
        result = pos.concluded()
        if result != -1:
            self.game_over = True
            self.winning_line = self.find_winning_line()
    
    def find_winning_line(self):
        b = self.board
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for line in lines:
            if b[line[0]] and b[line[0]] == b[line[1]] == b[line[2]]:
                return line
        return None
    
    def update_display(self):
        # Get scores from solver
        scores = t.solve(self.board, self.misere) if not self.game_over else [0] * 9
        
        for i, cell in enumerate(self.cells):
            cell.delete('all')
            
            # Determine if this cell is in winning line
            is_winning = self.winning_line and i in self.winning_line
            
            # Background color
            if is_winning:
                bg_color = self.lose_highlight if self.misere else self.win_highlight
                cell.configure(bg=bg_color)
            else:
                cell.configure(bg=self.bg_color)
            
            # Draw symbol if occupied
            if self.board[i] == 1:
                color = self.x_color
                cell.create_text(60, 60, text='X', font=self.symbol_font, fill=color)
            elif self.board[i] == 2:
                color = self.o_color
                cell.create_text(60, 60, text='O', font=self.symbol_font, fill=color)
            else:
                # Draw score if cell is empty
                score = scores[i]
                if score != -999999:
                    if score > 0:
                        score_color = self.positive_color
                    elif score < 0:
                        score_color = self.negative_color
                    else:
                        score_color = self.neutral_color
                    
                    # Make score more transparent
                    cell.create_text(
                        60, 60,
                        text=str(score),
                        font=self.score_font,
                        fill=score_color,
                        stipple='gray50'
                    )
    
    def on_hover(self, idx):
        if self.board[idx] == 0 and not self.game_over:
            cell = self.cells[idx]
            current_player = self.get_current_player()
            symbol = 'X' if current_player == 1 else 'O'
            color = self.x_color if current_player == 1 else self.o_color
            
            # Draw semi-transparent hover symbol
            cell.delete('hover')
            cell.create_text(
                60, 60,
                text=symbol,
                font=self.hover_font,
                fill=color,
                stipple='gray50',
                tags='hover'
            )
    
    def on_leave(self, idx):
        if self.board[idx] == 0:
            cell = self.cells[idx]
            cell.delete('hover')
            # Redraw the score
            scores = t.solve(self.board, self.misere) if not self.game_over else [0] * 9
            score = scores[idx]
            if score != -999999:
                if score > 0:
                    score_color = self.positive_color
                elif score < 0:
                    score_color = self.negative_color
                else:
                    score_color = self.neutral_color
                
                cell.create_text(
                    60, 60,
                    text=str(score),
                    font=self.score_font,
                    fill=score_color,
                    stipple='gray50'
                )

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
