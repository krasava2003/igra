import random

def print_board(board):
    for r in range(3, 10):
        for c in range(3, 10):
            if board[r][c] == 0:
                print("   ", end="")
            elif board[r][c] == -50:
                print(" . ", end="")
            elif board[r][c] == -1:
                print(" C ", end="")
            elif board[r][c] == 1:
                print(" H ", end="")
            elif board[r][c] == 'A':
                print(" A ", end="")
            elif board[r][c] == 'B':
                print(" B ", end="")
            elif r % 2 == 0:
                print(" : ", end="")
            else:
                print(" - ", end="")
        print()

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

def main():
    print(" " * 26 + "CONDOT")
    print(" " * 20 + "CREATIVE COMPUTING")
    print(" " * 18 + "MORRISTOWN, NEW JERSEY")
    print()
    print()
    print("THIS PROGRAM WILL PLAY CONNECT THE DOTS WITH YOU.")
    print("THE GAME IS PLAYED ON A 4 X 4 ARRAY. WHEN")
    print("YOU WANT TO MAKE A MOVE YOU MUST TYPE IN")
    print("THE COORDINATES OF THE SPACE BETWEEN THE TWO DOTS YOU")
    print("WANT TO CONNECT. ENTER EACH OF YOUR MOVES BY TYPING")
    print("THE ROW NUMBER, A COMMA AND THE COLUMN NUMBER.")
    print("THE UPPER LEFT HAND CORNER OF THE ARRAY IS 1,1.")
    print("HERE WE GO.")

    board = [[0 for _ in range(13)] for _ in range(13)]
    for r in range(1, 13):
        for c in range(1, 13):
            if r % 2 != 0 and c % 2 != 0:
                board[r][c] = -50

    while True:
        print_board(board)
        print("YOUR MOVE")
        try:
            x, y = map(int, input().split(','))
            x += 2
            y += 2
            if x < 3 or x > 9 or y < 3 or y > 9:
                print("YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!")
                continue
            if (x + y + 1) % 2 != 0:
                print("YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!")
                continue
            if board[x][y] != 0:
                print("YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!")
                continue
            board[x][y] = 1
            check_and_mark_squares(board, 1)
        except ValueError:
            print("YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!")
            continue

        if check_all_squares_closed(board):
            break

        print_board(board)
        print("MY MOVE")
        for r in range(3, 10):
            for c in range(3, 10):
                if (r + c) % 2 != 0 and board[r][c] == 0:
                    if r % 2 != 0:
                        if board[r-2][c] + board[r-1][c-1] + board[r-1][c+1] == 2:
                            continue
                        if board[r+2][c] + board[r+1][c-1] + board[r+1][c+1] == 2:
                            continue
                    else:
                        if board[r][c-2] + board[r-1][c-1] + board[r+1][c-1] == 2:
                            continue
                        if board[r][c+2] + board[r-1][c+1] + board[r+1][c+1] == 2:
                            continue
                    board[r][c] = -1
                    check_and_mark_squares(board, -1)
                    break
            else:
                continue
            break
        else:
            while True:
                r = random.randint(3, 9)
                c = random.randint(3, 9)
                if (r + c) % 2 == 0 and board[r][c] == 0:
                    board[r][c] = -1
                    check_and_mark_squares(board, -1)
                    break

        if check_all_squares_closed(board):
            break

    human_score, computer_score = count_scores(board)
    print_board(board)
    print(f"Human score: {human_score}, Computer score: {computer_score}")
    if human_score > computer_score:
        print("YOU WON!!!")
    else:
        print("I WON")

    print("DO YOU WANT TO PLAY AGAIN (TYPE 1 FOR YES OR 2 FOR NO)")
    if input() == "1":
        main()

if __name__ == "__main__":
    main()