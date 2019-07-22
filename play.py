'''play.py: Play a game of tic-tac-toe against an AI opponent.'''
import board
import sklearn as skl

# Initialize ML model.
x = []
y = []

# Run n episodes.
for n in range(0, 10):
    board = board.Board()
    while not board.is_win():
        for player in range(2):
            model.fit
