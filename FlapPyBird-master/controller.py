from __future__ import print_function

import sys
import game.wrapped_flappy_bird as game
import random
from math import sqrt, atan2

ACTIONS = 2
FIRST_JUMP = True

def run():
    game_state = game.GameState()
    flap = False
    state, reward, terminal = game_state.frame_step(flap)
    while True:
        #flap = randomStrategy()
        flap = heuristicStrategy(state)
        state, reward, terminal = game_state.frame_step(flap)
        discState = discretizeState(state)
       
def discretizeState(state):
    player = state['playerRect']
    playerVelY = state['playerVelY']
    birdMid = (player.x+(player.width/2),player.y+(player.height/2))
    upperPipeList = state['uPipeRects']
    lowerPipeList = state['lPipeRects']
    discState = [playerVelY]
    for x in range(0,len(upperPipeList)):
        if(player.left<upperPipeList[x].right):
            pipeMid = (upperPipeList[x].x+(upperPipeList[x].width/2),(upperPipeList[x].bottom+lowerPipeList[x].top)/2)
            if(x!=len(upperPipeList)-1):
                discState.append(distanceBirdToPipeMiddle(birdMid,pipeMid))
            discState.append(angleBirdToPipeMiddle(birdMid,pipeMid))
    print(discState)
    
def distanceBirdToPipeMiddle(birdMid,pipeMid):
    xDistance = pipeMid[0]-birdMid[0]
    yDistance = pipeMid[1]-birdMid[1]
    return int(sqrt((xDistance)**2+(yDistance)**2))

def angleBirdToPipeMiddle(birdMid,pipeMid):
    diffPoint = (pipeMid[0]-birdMid[0],pipeMid[1]-birdMid[1])
    return int(atan2(diffPoint[1],diffPoint[0])*100)   
 
def randomStrategy():
    if(random.randrange(ACTIONS)==0):
        return True
    return False

def heuristicStrategy(state):
    nextPipeIndex = 0
    firstLowerPipe = state['lPipeRects'][0]
    player = state['playerRect']
    playerVelY = state['playerVelY']
    pipeVelX = state['pipeVelX']
    distFromPipeEdge = firstLowerPipe.right-player.left
    
    if(passedPipe(distFromPipeEdge, pipeVelX)):
        nextPipeIndex = 1
        global FIRST_JUMP
        FIRST_JUMP = True
        
    nextLowerPipe = state['lPipeRects'][nextPipeIndex]
    nextNextLowerPipe = state['lPipeRects'][nextPipeIndex+1]
    nextUpperPipe = state['uPipeRects'][nextPipeIndex]
    
    if(playerBelowNextPipe(player,playerVelY,nextLowerPipe)):
        return True
    elif(pipeDecrease(nextLowerPipe,nextNextLowerPipe) and earliestExitPoint(player,nextLowerPipe, pipeVelX, nextUpperPipe)):
        return True
    else:
        return False

def passedPipe(distFromPipeEdge, pipeVelX):
    return distFromPipeEdge<pipeVelX-1 #checking if the bird would have passed the pipe 
#in the next frame given the pipe's static velocity of -4 -1 for buffer

def playerBelowNextPipe(player,playerVelY,nextLowerPipe):
    return player.bottom+playerVelY+1>nextLowerPipe.top #checks if player will be below the next pipe in the next frame (1 for buffer)

def pipeDecrease(nextLowerPipe,nextNextLowerPipe):
    return nextLowerPipe.top<nextNextLowerPipe.top

def earliestExitPoint(player,nextLowerPipe, pipeVelX, nextUpperPipe):
    global FIRST_JUMP
    if(safeExitJump(player,nextLowerPipe,pipeVelX,nextUpperPipe) and FIRST_JUMP):
        FIRST_JUMP = False
        return True
    return False

def safeExitJump(player,nextLowerPipe,pipeVelX,nextUpperPipe):
    distFromPipeEdge = nextLowerPipe.right-player.left 
    framesFromPipeEdge = abs(distFromPipeEdge//pipeVelX)
    finalPlayerY = player.bottom
    playerVel = -9
    finalPlayerY += playerVel
    maxPlayerVel = 10
    for x in range(0,framesFromPipeEdge):
        if(playerVel < maxPlayerVel):
            playerVel+=1
        finalPlayerY+=playerVel
        if(playerHitsTopPipe(finalPlayerY,player,nextUpperPipe)):
            return False
    return finalPlayerY<nextLowerPipe.top

def playerHitsTopPipe(playery,player,nextUpperPipe):
    return playery-player.height<nextUpperPipe.bottom

def main():
    run()

if __name__ == "__main__":
    main()