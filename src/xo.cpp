#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cstdint>
#include <vector>
#include <cassert>
#include <iostream>
#include <algorithm>

namespace py = pybind11;

struct Position
{
    std::vector<int> board{9};

    Position(const std::vector<int>& b) : board(b) {}

    int key() const {
        int result = 0;
        int power = 1;
        for (int i = 8; i >= 0; --i) {
            result += board[i] * power;
            power *= 3;
        }
        // Multiply by a large number and add move count to make keys unique
        return result * 100 + nMoves();
    }

    bool isFull() const {
        for(int i = 0; i < 9; i++) if(!board[i]) return false;
        return true;
    }

    int concluded() const {
        // rows
        if(board[0] && board[0] == board[1] && board[0] == board[2]) return board[0];
        if(board[3] && board[3] == board[4] && board[3] == board[5]) return board[3];
        if(board[6] && board[6] == board[7] && board[6] == board[8]) return board[6];

        // columns
        if(board[0] && board[0] == board[3] && board[0] == board[6]) return board[0];
        if(board[1] && board[1] == board[4] && board[1] == board[7]) return board[1];
        if(board[2] && board[2] == board[5] && board[2] == board[8]) return board[2];

        // diagonal
        if(board[0] && board[0] == board[4] && board[0] == board[8]) return board[0];
        if(board[2] && board[2] == board[4] && board[2] == board[6]) return board[2];

        // draw
        if(isFull()) return 0;

        // not concluded
        return -1;
    }

    int canPlay(int col) const {
        if(col < 0 || col >= 9) return false;
        return board[col] == 0;
    }

    int nMoves() const {
        int n = 0;
        for(int i = 0; i < 9; i++) if(board[i]) n++;
        return n;
    }

    int currentPlayer() const {
        return nMoves() % 2 ? 2 : 1;
    }

    std::vector<int> getPossibleMoves() const {
        std::vector<int> possibleMoves;
        for(int i = 0; i < 9; i++) if(!board[i]) possibleMoves.push_back(i); 
        return possibleMoves;
    }

    Position play(int col) const {
        Position p = Position(board);
        p.board[col] = currentPlayer();
        return p;
}
};

int minimax(const Position &p, int alpha, int beta, int mode = 1) {
    // int k = p.key();
    // if(memo.count(k)) return memo[k];

    int conclusion = p.concluded();
    if(conclusion == 0) return 0;
    if(conclusion == 1) return mode * (10 - p.nMoves());
    if(conclusion == 2) return mode * (p.nMoves() - 10);

    if(p.currentPlayer() == 1){
        int best = -123456;
        for(int move: p.getPossibleMoves()){
            int score = minimax(p.play(move), alpha, beta, mode);
            best = std::max(best, score);
            alpha = std::max(alpha, score);
            if(beta < alpha) break;
        }
        return best;
    }

    // else
    int best = 123456;
    for(int move: p.getPossibleMoves()){
        int score = minimax(p.play(move), alpha, beta, mode);
        best = std::min(best, score);
        beta = std::min(beta, score);
        if(beta < alpha) break;
    }
    return best;
}


std::vector<int> solve(const Position &p, int mode = 1) {    
    std::vector<int> scores(9);
    
    for(int i = 0; i < 9; i++) {
        // std::cout << "##### " << i << " #####\n"; 
        if(p.canPlay(i)) {
            Position newPos = p.play(i);
            scores[i] = minimax(newPos, -123456, 123456, mode);
        } else {
            scores[i] = -999999;  // Invalid move marker
        }
    }
    
    return scores;
}


PYBIND11_MODULE(tictactoe_solver, m) {
    m.doc() = "Tic Tac Toe Solver";

    m.def("foo", []()->int {
        std::cout << "hello world from C++!\n";
        return 0;  
    });

    m.def("solve", [](std::vector<int> board, bool mesere)-> std::vector<int> {    
        int mode = mesere ? -1 : 1;
        Position p = Position(board);
        return solve(p, mode);
    }, py::arg("board"), py::arg("mesere"));
}
