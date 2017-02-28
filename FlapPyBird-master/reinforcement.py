from __future__ import print_function

import sys
import game.wrapped_flappy_bird as game
import random

GAME = 'bird' # the name of the game being played for log files
ACTIONS = 2 # number of valid actions
FRAME_PER_ACTION = 1
FIRST_JUMP = True

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
            #a_t = randomStrategy(a_t)
            a_t = heuristicStrategy(a_t, state)
        # run the selected action and observe next state and reward
        stateNew, r_t, terminal = game_state.frame_step(a_t)
        #train model based on new state + rewards compared to old state
        
        # update the old values
        state = stateNew
        t += 1

        # save progress every 10000 iterations
        #if t % 10000 == 0:
        #    saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = t)
        
def randomStrategy(a_t):
    a_t[random.randrange(ACTIONS)] = 1
    return a_t

def heuristicStrategy(a_t, state):
    nextPipeIndex = 0
    distFromPipeEdge = state['lPipeRects'][0].right-state['playerRect'].left
    if(distFromPipeEdge<state['pipeVelX']-1):
        nextPipeIndex = 1
        global FIRST_JUMP
        FIRST_JUMP = True
    if(state['playerRect'].bottom+state['playerVelY']+1>state['lPipeRects'][nextPipeIndex].top):
        a_t[1] = 1
    elif(pipeAboveNextPipe(state,nextPipeIndex) and correctJumpPoint(state,nextPipeIndex)):
        a_t[1] = 1
    else:
        a_t[0] = 1
    return a_t

def pipeAboveNextPipe(state,nextPipeIndex):
    if(state['lPipeRects'][nextPipeIndex].top<state['lPipeRects'][nextPipeIndex+1].top):
        return True
    return False

def correctJumpPoint(state,nextPipeIndex):
    global FIRST_JUMP
    if(validJump(state,nextPipeIndex) and FIRST_JUMP  
       and state['playerRect'].right<state['lPipeRects'][nextPipeIndex].right):
        FIRST_JUMP = False
        return True
    return False

def validJump(state,nextPipeIndex):
    distFromPipeEdge = state['lPipeRects'][nextPipeIndex].right-state['playerRect'].left 
    framesFromPipeEdge = abs(distFromPipeEdge//state['pipeVelX'])
    playery = state['playerRect'].bottom
    playerVel = -9
    playery += playerVel
    for x in range(0,framesFromPipeEdge):
        if(playerVel<10):
            playerVel+=1
        playery+=playerVel
        if(playery-state['playerRect'].height<state['uPipeRects'][nextPipeIndex].bottom):
            return False
    return playery<state['lPipeRects'][nextPipeIndex].top

def playGame():
    run()

def main():
    playGame()

if __name__ == "__main__":
    main()