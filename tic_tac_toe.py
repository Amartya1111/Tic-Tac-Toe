import math
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Represents the 3x3 game board
        self.current_winner = None  # Keeps track of the winner

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # Tells us what number corresponds to what box in the board
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # Check diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


def minimax(position, maximizing_player, alpha, beta):
    if position.current_winner:
        return {'position': position, 'score': 1 if position.current_winner == 'X' else -1}

    if not position.empty_squares():
        return {'position': position, 'score': 0}

    if maximizing_player:
        max_eval = {'position': None, 'score': -math.inf}
        for move in position.available_moves():
            new_position = position
            new_position.make_move(move, 'X')
            eval = minimax(new_position, False, alpha, beta)
            if eval['score'] > max_eval['score']:
                max_eval = eval
            alpha = max(alpha, eval['score'])
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = {'position': None, 'score': math.inf}
        for move in position.available_moves():
            new_position = position
            new_position.make_move(move, 'O')
            eval = minimax(new_position, True, alpha, beta)
            if eval['score'] < min_eval['score']:
                min_eval = eval
            beta = min(beta, eval['score'])
            if beta <= alpha:
                break
        return min_eval


def play_game():
    game = TicTacToe()
    print("Welcome to Tic-Tac-Toe!")
    print("Here's how the board is numbered:")
    TicTacToe.print_board_nums()
    print("Let's start!")

    while game.empty_squares():
        if game.num_empty_squares() % 2 == 1:  # Player's turn
            try:
                move = int(input("Enter your move (0-8): "))
                if move < 0 or move > 8:
                    raise ValueError
                if game.make_move(move, 'O'):
                    game.print_board()
                else:
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 8.")
                continue
        else:  # AI's turn
            print("AI is making a move...")
            best_move = minimax(game, True, -math.inf, math.inf)['position']
            game = best_move
            game.print_board()

        if game.current_winner:
            if game.current_winner == 'X':
                print("AI wins!")
            else:
                print("You win!")
            break

    if not game.current_winner:
        print("It's a tie!")

play_game()
