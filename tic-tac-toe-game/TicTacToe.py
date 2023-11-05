class TicTacToe:
    def __init__(self):
        self.turn = 0
        self.board = []
        for _ in range(3):
            r = []
            for _ in range(3):
                r.append(" ")
            self.board.append(r)

    def __str__(self):
        lines = "  --+---+--\n"
        string = "  1   2   3 \n"
        string += f"A {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]}\n" + lines
        string += f"B {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]}\n" + lines
        string += f"C {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}\n"

        return string

    def is_full(self):
        return self.turn >= 9

    def winner(self):
        char = None
        player_char = {"X": "Player 1", "O": "Player 2"}
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                char = row[0]
        
        for col in range(len(self.board[0])):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                char = self.board[0][col]
        
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != " " or
                self.borad[2][0] == self.board[1][1] == self.board[0][2] != " "):
            char = self.board[0][0]

        if char:
            return player_char[char]
        else:
            return None

    def get_coords(self):
        rows = {"A": 0, "B": 1, "C": 2}
        columns = {"1":0, "2": 1, "3": 2}
        row = input("Enter a row\n").upper()
        col = input("Enter a column\n")
        return rows[row], columns[col]
    
    def player_turn(self):
        print(self)
        self.turn += 1
        if self.turn % 2 == 1:
            char = "X"
        else:
            char = "O"
        x, y = self.get_coords()
        self.board[x][y] = char
