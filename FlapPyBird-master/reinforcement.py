from __future__ import print_function

import sys
import game.wrapped_flappy_bird as game
import random

GAME = 'bird' # the name of the game being played for log files
ACTIONS = 2 # number of valid actions
FRAME_PER_ACTION = 4

def trainNetwork():

    # open up a game state to communicate with emulator
    game_state = game.GameState()

    # start training
    t = 0
    while "flappy bird" != "angry bird":
        
        # choose an action
        a_t = [0,0]
        if t % FRAME_PER_ACTION == 0:
            a_t[random.randrange(ACTIONS)] = 1
            print(a_t)
        else:
            a_t[0] = 1
        # run the selected action and observe next state and reward
        r_t, terminal = game_state.frame_step(a_t)

        # update the old values
        t += 1

        # save progress every 10000 iterations
        #if t % 10000 == 0:
        #    saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = t)

def playGame():
    trainNetwork()

def main():
    playGame()

if __name__ == "__main__":
    main()