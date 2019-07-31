class Board:    
    """Represents a Tic-Tac-Toe board."""
    
    def __init__(self):
        self.board = [' ' for i in range(9)]
        self.broken_rules = False

    def is_done(self):
        return self.broken_rules or self.is_win() or self.board.count('x')+self.board.count('o') == 9

    def valid_moves(self):
        moves = []
        for b in range(len(self.board)):
            if self.board[b] == ' ':
                moves.append(b)
        return moves
            
    def place(self, loc, t):
        if self.board[loc] != ' ':
            self.broken_rules = True
        else:
            self.board[loc] = t 

    def reward(self, player):
        if self.is_win(player):
            return 1
        elif self.broken_rules:
            return -1
        elif self.is_done():
            return 0.5
        else:
            return 0.1

    def is_win(self, t = ' '):
        # Horizontal wins
        if t == ' ':
            return self.is_win('x') or self.is_win('o')
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
    
    def get_board_vector(self, t):
        vec = []
        for b in self.board:
            # Your spots
            if b == t:
                vec.append(1)
            # Empty spots
            elif b == ' ':
                vec.append(0)
            # Opponent spots
            else:
                vec.append(-1)
        return vec

    def print_board(self):
        p = [self.board[i] if self.board[i] != ' ' else i  for i in range(len(self.board))]
        print("""{0} | {1} | {2}\n{3} | {4} | {5}\n{6} | {7} | {8}""".format(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))


