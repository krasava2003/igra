from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
import random


class CondotApp(App):
    def build(self):
        self.board = [[0 for _ in range(13)] for _ in range(13)]
        for r in range(1, 13):
            for c in range(1, 13):
                if r % 2 != 0 and c % 2 != 0:
                    self.board[r][c] = -50

        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="THIS PROGRAM WILL PLAY CONNECT THE DOTS WITH YOU.\n"
                                "THE GAME IS PLAYED ON A 4 X 4 ARRAY. WHEN\n"
                                "YOU WANT TO MAKE A MOVE YOU MUST TYPE IN\n"
                                "THE COORDINATES OF THE SPACE BETWEEN THE TWO DOTS YOU\n"
                                "WANT TO CONNECT. ENTER EACH OF YOUR MOVES BY TYPING\n"
                                "THE ROW NUMBER, A COMMA AND THE COLUMN NUMBER.\n"
                                "THE UPPER LEFT HAND CORNER OF THE ARRAY IS 1,1.\n"
                                "HERE WE GO.")
        self.layout.add_widget(self.label)

        self.grid = GridLayout(cols=7, rows=7)
        self.buttons = [[Button(text="") for _ in range(7)] for _ in range(7)]
        for r in range(7):
            for c in range(7):
                self.grid.add_widget(self.buttons[r][c])
        self.layout.add_widget(self.grid)

        self.input_layout = BoxLayout(orientation='horizontal')
        self.input_label = Label(text="YOUR MOVE (row,col):")
        self.input_layout.add_widget(self.input_label)
        self.text_input = TextInput(multiline=False)
        self.input_layout.add_widget(self.text_input)
        self.layout.add_widget(self.input_layout)

        self.submit_button = Button(text="Submit")
        self.submit_button.bind(on_press=self.make_move)
        self.layout.add_widget(self.submit_button)

        # Add a restart button
        self.restart_button = Button(text="Restart Game")
        self.restart_button.bind(on_press=self.restart_game)
        self.layout.add_widget(self.restart_button)

        return self.layout

    def make_move(self, instance):
        try:
            x, y = map(int, self.text_input.text.split(','))
            x += 2
            y += 2
            if x < 3 or x > 9 or y < 3 or y > 9:
                self.label.text = "YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!"
                return
            if (x + y + 1) % 2 != 0:
                self.label.text = "YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!"
                return
            if self.board[x][y] != 0:
                self.label.text = "YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!"
                return
            self.board[x][y] = 1
            self.update_board()
            self.check_and_mark_squares(1)
        except ValueError:
            self.label.text = "YOU REALLY DON'T WANT TO PUT A LINE THERE!!!!"
            return

        if self.check_all_squares_closed():
            self.end_game()
            return

        self.computer_move()

        if self.check_all_squares_closed():
            self.end_game()
            return

    def update_board(self):
        for r in range(3, 10):
            for c in range(3, 10):
                if self.board[r][c] == 1:
                    self.buttons[r - 3][c - 3].background_color = (0, 1, 0, 1)  # Green for human move
                elif self.board[r][c] == -1:
                    self.buttons[r - 3][c - 3].background_color = (1, 0, 0, 1)  # Red for computer move
                elif self.board[r][c] == 'A':
                    self.buttons[r - 3][c - 3].background_color = (0, 0, 1, 1)  # Blue for player A
                elif self.board[r][c] == 'B':
                    self.buttons[r - 3][c - 3].background_color = (1, 1, 0, 1)  # Yellow for player B

    def check_and_mark_squares(self, player):
        for r in range(4, 11, 2):
            for c in range(4, 11, 2):
                if self.board[r - 1][c] != 0 and self.board[r + 1][c] != 0 and self.board[r][c - 1] != 0 and \
                        self.board[r][c + 1] != 0:
                    if self.board[r][c] == 0:
                        self.board[r][c] = 'A' if player == 1 else 'B'
                        self.update_board()

    def check_all_squares_closed(self):
        closed_squares = 0
        for r in range(4, 11, 2):
            for c in range(4, 11, 2):
                if self.board[r][c] != 0:
                    closed_squares += 1
        return closed_squares == 9

    def count_scores(self):
        human_score = 0
        computer_score = 0
        for r in range(4, 11, 2):
            for c in range(4, 11, 2):
                if self.board[r][c] == 'A':
                    human_score += 1
                elif self.board[r][c] == 'B':
                    computer_score += 1
        return human_score, computer_score

    def computer_move(self):
        for r in range(3, 10):
            for c in range(3, 10):
                if (r + c) % 2 != 0 and self.board[r][c] == 0:
                    if r % 2 != 0:
                        if self.board[r - 2][c] + self.board[r - 1][c - 1] + self.board[r - 1][c + 1] == 2:
                            continue
                        if self.board[r + 2][c] + self.board[r + 1][c - 1] + self.board[r + 1][c + 1] == 2:
                            continue
                    else:
                        if self.board[r][c - 2] + self.board[r - 1][c - 1] + self.board[r + 1][c - 1] == 2:
                            continue
                        if self.board[r][c + 2] + self.board[r - 1][c + 1] + self.board[r + 1][c + 1] == 2:
                            continue
                    self.board[r][c] = -1
                    self.update_board()
                    self.check_and_mark_squares(-1)
                    return
        while True:
            r = random.randint(3, 9)
            c = random.randint(3, 9)
            if (r + c) % 2 == 0 and self.board[r][c] == 0:
                self.board[r][c] = -1
                self.update_board()
                self.check_and_mark_squares(-1)
                return

    def end_game(self):
        human_score, computer_score = self.count_scores()
        self.label.text = f"Human score: {human_score}, Computer score: {computer_score}\n"
        if human_score > computer_score:
            self.label.text += "YOU WON!!!"
        else:
            self.label.text += "I WON"

    def restart_game(self, instance):
        # Reset the game board to its initial state
        self.board = [[0 for _ in range(13)] for _ in range(13)]
        for r in range(1, 13):
            for c in range(1, 13):
                if r % 2 != 0 and c % 2 != 0:
                    self.board[r][c] = -50

        # Reset the buttons' colors to default (white)
        for r in range(7):
            for c in range(7):
                self.buttons[r][c].background_color = (1, 1, 1, 1)  # Reset color to white

        # Reset the input text and label
        self.text_input.text = ""
        self.label.text = "THIS PROGRAM WILL PLAY CONNECT THE DOTS WITH YOU.\n" \
                          "THE GAME IS PLAYED ON A 4 X 4 ARRAY. WHEN\n" \
                          "YOU WANT TO MAKE A MOVE YOU MUST TYPE IN\n" \
                          "THE COORDINATES OF THE SPACE BETWEEN THE TWO DOTS YOU\n" \
                          "WANT TO CONNECT. ENTER EACH OF YOUR MOVES BY TYPING\n" \
                          "THE ROW NUMBER, A COMMA AND THE COLUMN NUMBER.\n" \
                          "THE UPPER LEFT HAND CORNER OF THE ARRAY IS 1,1.\n" \
                          "HERE WE GO."


if __name__ == '__main__':
    CondotApp().run()
