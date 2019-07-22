class Board:

    def __init__(self):
        self.board = [0 for i in range(9)]

    def place(self, loc, t):
        self.board[loc] = t 

    def is_win(self):
        for t in ['x', 'o']:
            # Horizontal wins
            if self.board[0] == t and self.board[1] == t and self.board[2] == t:
                return True
            if self.board[3] == t and self.board[4] == t and self.board[5] == t:
                return True
            if self.board[6] == t and self.board[7] == t and self.board[8] == t:
                return True
            # Vertical wins
            if self.board[0] == t and self.board[3] == t and self.board[6] == t:
                return True
            if self.board[1] == t and self.board[4] == t and self.board[7] == t:
                return True
            if self.board[2] == t and self.board[5] == t and self.board[8] == t:
                return True
            # Diagonal wins
            if self.board[0] == t and self.board[4] == t and self.board[8] == t:
                return True
            if self.board[2] == t and self.board[4] == t and self.board[6] == t:
                return True
        return False

    def get_board(self):
        return self.board

    def print_board(self):
        print("""{0} | {1} | {2}\n{3} | {4} | {5}\n{6} | {7} | {8}""".format(self.board[0], self.board[1], self.board[2], self.board[3],
                     self.board[4], self.board[5], self.board[6], self.board[7], self.board[8]))


