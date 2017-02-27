from __future__ import print_function

import sys
import game.wrapped_flappy_bird as game
import random

GAME = 'bird' # the name of the game being played for log files
ACTIONS = 2 # number of valid actions
FRAME_PER_ACTION = 1

def run():

    # open up a game state to communicate with emulator
    game_state = game.GameState()

    # start training
    a_t = [0,0]
    a_t[0] = 1
    state, r_t, terminal = game_state.frame_step(a_t)
    t = 0
    while "flappy bird" != "angry bird":
        
        # choose an action
        a_t = [0,0]
        if t % FRAME_PER_ACTION == 0:
            #select action based on state
            #a_t[random.randrange(ACTIONS)] = 1
            nextPipeIndex = 0
            if(state['playerRect'].left>state['lPipeRects'][0].right+state['pipeVelX']):
                nextPipeIndex = 1
            if(state['playerRect'].bottom+state['playerVelY']+1>state['lPipeRects'][nextPipeIndex].top):
                a_t[1] = 1
            else:
                a_t[0] = 1
        else:
            a_t[0] = 1
        # run the selected action and observe next state and reward
        stateNew, r_t, terminal = game_state.frame_step(a_t)
        #train model based on new state + rewards compared to old state
        
        # update the old values
        state = stateNew
        t += 1

        # save progress every 10000 iterations
        #if t % 10000 == 0:
        #    saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = t)

def playGame():
    run()

def main():
    playGame()

if __name__ == "__main__":
    main()