'''play.py: Play a game of tic-tac-toe against an AI opponent.'''
import board
import numpy as np
import random
import pickle
import sys
from sklearn.neural_network import MLPRegressor

def experience_replay(replay_memory):
    """Trains model on experiences, e."""
    """ e = (s, a, r, s') """

    # Shuffle the memory.
    random.shuffle(replay_memory)

    # Fit the model to replay memory.
    states  = []
    targets = []
    for (state, action, reward, next_state, done) in replay_memory[:5000]:
        if not done:
            target = reward + gamma*np.max(model.predict([next_state]))
        else:
            target = reward

        target_f = model.predict([state])
        target_f[0][action] = target
        states.append(state)
        targets.append(target_f[0])
    model.partial_fit(states, targets)
    return model

t_avg = [0, 0, 0]
scores  = []
if sys.argv[1] == 'train':
    replay_memory = []
    gamma = 0.99 # discount factor
    epsilon = 0.05 # exploration/exploitation ratio
    episodes = 750000
    ramp     = 25000

    # Init ML model
    model = MLPRegressor(hidden_layer_sizes=(50))
    xstate = np.zeros(9)
    ystate = np.zeros(9)
    model.fit([xstate], [ystate])

    # Play n episodes
    for n in range(episodes):
        b = board.Board()
        first = True
        while not b.is_done():
            for player in ['x', 'o']:

                # Get current game state
                state = b.get_board_vector(player)

                # Select action with epsilon-greedy strategy
                if random.uniform(0, 1) < 1+(-epsilon*n/ramp) or first:
                    # Explore: make random valid move
                    action = random.choice(b.valid_moves())
                    first = False
                else:
                    # Exploit: make best move.
                    action = np.argmax(model.predict([state]))

                b.place(action, player)
                reward = b.reward(player)
                # Correct reward for losing player.
                if b.is_win():
                    replay_memory[-1][2] = -5.0
                    replay_memory[-1][4] = True
                new_state = b.get_board_vector(player)

                # Store experience e(s, a, r, s') in replay memory.
                replay_memory.append([state, action, reward, new_state, b.is_done()])

                if b.is_done():
                    break

        # Update model every so often.
        if not n % 100:
            score = (0.5*t_avg[1] +  t_avg[2])/100
            scores.append((n, score))
            model = experience_replay(replay_memory)
            with open(sys.argv[2]+ 'out', 'w') as f: 
                sys.stdout.write("Episode {0}, Broken Rules: {1}, Win/Loss: {2}, Tie: {3},  Average Score: {4:.2f}\r".format(n, t_avg[0], t_avg[1], t_avg[2], score))
                sys.stdout.flush()
                for s in scores:
                    f.write("{0} {1}\n".format(s[0], s[1]))
                t_avg = [0, 0, 0]
        else:
            if b.broken_rules:
                t_avg[0] += 1
            elif b.is_win():
                t_avg[1] += 1
            elif b.is_done():
                t_avg[2] += 1
        if not n % 100:
            with open(sys.argv[2], 'wb') as f:
                pickle.dump(model, f)


elif sys.argv[1] == 'play':
    with open(sys.argv[2], 'rb') as f:
        model = pickle.load(f)
    b = board.Board()
    b.print_board()
    while not b.is_done():
        for player in ['x', 'o']:
            if player == 'x':
                move = int(input("Move: "))
                b.place(move, 'x')
            else:
                # Get current game state
                state = b.get_board_vector(player)

                # Select action with epsilon-greedy strategy
                # Exploit: make best move.
                action = np.argmax(model.predict([state]))

                b.place(action, player)
                reward = b.reward(player)
                new_state = b.get_board_vector(player)
            if player == 'o':
                b.print_board()
            if b.is_done():
                break

    if b.broken_rules:
        print("Broken Rules.")
    elif b.is_win('x') or b.is_win('o'):
        print("Win/Lose")
    else:
        print("Tie")
