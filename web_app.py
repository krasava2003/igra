import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

current_game = None

def print_board(board):
    display_board = []
    for r in range(3, 10):
        row = []
        for c in range(3, 10):
            if board[r][c] == 0:
                row.append("   ")
            elif board[r][c] == -50:
                row.append(" . ")
            elif board[r][c] == -1:
                row.append(" C ")
            elif board[r][c] == 1:
                row.append(" H ")
            elif board[r][c] == 'A':
                row.append(" A ")
            elif board[r][c] == 'B':
                row.append(" B ")
            elif r % 2 == 0:
                row.append(" : ")
            else:
                row.append(" - ")
        display_board.append(row)
    return display_board

def check_and_mark_squares(board, player):
    for r in range(4, 11, 2):
        for c in range(4, 11, 2):
            if board[r-1][c] != 0 and board[r+1][c] != 0 and board[r][c-1] != 0 and board[r][c+1] != 0:
                if board[r][c] == 0:
                    board[r][c] = 'A' if player == 1 else 'B'

def check_all_squares_closed(board):
    closed_squares = 0
    for r in range(4, 11, 2):
        for c in range(4, 11, 2):
            if board[r][c] != 0:
                closed_squares += 1
    return closed_squares == 9

def count_scores(board):
    human_score = 0
    computer_score = 0
    for r in range(4, 11, 2):
        for c in range(4, 11, 2):
            if board[r][c] == 'A':
                human_score += 1
            elif board[r][c] == 'B':
                computer_score += 1
    return human_score, computer_score

def computer_move(board):
    for r in range(3, 10):
        for c in range(3, 10):
            if (r + c) % 2 != 0 and board[r][c] == 0:
                board[r][c] = -1
                check_and_mark_squares(board, -1)
                return board
    return board

def initialize_game():
    board = [[0 for _ in range(13)] for _ in range(13)]
    for r in range(1, 13):
        for c in range(1, 13):
            if r % 2 != 0 and c % 2 != 0:
                board[r][c] = -50
    return board, 0, 0, False

@app.route('/')
def index():
    global current_game

    if current_game is None:
        current_game = initialize_game()

    board, human_score, computer_score, game_over = current_game
    display_board = print_board(board)

    return render_template('game.html', board=display_board, game_over=game_over, human_score=human_score, computer_score=computer_score)

@app.route('/play', methods=['POST'])
def play():
    global current_game

    move = request.form['move']
    x, y = map(int, move.split(','))
    x += 2
    y += 2

    board, human_score, computer_score, game_over = current_game

    if board[x][y] == 0:
        board[x][y] = 1
        check_and_mark_squares(board, 1)

    board = computer_move(board)

    game_over = check_all_squares_closed(board)

    human_score, computer_score = count_scores(board)

    current_game = (board, human_score, computer_score, game_over)

    display_board = print_board(board)
    return render_template('game.html', board=display_board, game_over=game_over, human_score=human_score, computer_score=computer_score)

@app.route('/reset', methods=['GET'])
def reset():
    global current_game

    current_game = initialize_game()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
