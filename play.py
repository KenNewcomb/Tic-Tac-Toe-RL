'''play.py: Play a game of tic-tac-toe against an AI opponent.'''
import board
import numpy as np
from sklearn.neural_network import MLPRegressor
import random
import time

def experience_replay(replay_memory):
    """Trains model on experiences, e."""
    """ e = (s, a, r, s') """

    # Shuffle the memory.
    random.shuffle(replay_memory)

    # Fit the model to replay memory.
    states  = []
    targets = []
    for (state, action, reward, next_state, done) in replay_memory:
        if not done:
            target = reward + gamma*np.max(model.predict([next_state]))
        else:
            target = reward

        target_f = model.predict([state])
        target_f[0][action] = target
        states.append(state)
        targets.append(target_f[0])
    model.fit(states, targets)
    return model

# Suppress scikit's convergence warnings.
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

replay_memory = []
gamma = 0.99 # reward decay
epsilon = 0.50 # exploration/exploitation ratio
episodes = 5000

# Init ML model
model = MLPRegressor(hidden_layer_sizes=(100), max_iter=1000)
xstate = np.zeros(9)
ystate = np.zeros(9)
model.fit([xstate], [ystate])

# Play n episodes
for n in range(episodes):
    print("Episode #{0}".format(n))
    print("------------")
    b = board.Board()
    total_reward = 0
    while not b.is_done():
        for player in ['x', 'o']:

            # Limit experience replay memory length
            #replay_memory = replay_memory[-7500:]

            # Get current game state
            state = b.get_board_vector(player)

            # Select action with epsilon-greedy strategy
            if random.uniform(0, 1) < epsilon:
                # Explore: make random valid move
                action = random.choice(b.valid_moves())
            else:
                # Exploit: make best move.
                action = np.argmax(model.predict([state]))

            b.place(action, player)
            reward = b.reward(player)
            total_reward += reward
            new_state = b.get_board_vector(player)
            
            # Store experience e(s, a, r, s') in replay memory.
            replay_memory.append((state, action, reward, new_state, b.is_done()))
            
            if b.is_done():
                break 

    # Update model every so often.
    if not n % 50:
        model = experience_replay(replay_memory)
        with open('out', 'a') as f:
            f.write("{0} {1}\n".format(n/50, total_reward))

    if b.broken_rules:
        print("Broken")
    elif b.is_win('x') or b.is_win('o'):
        print("Win")
    else:
        print("Tie")
    
