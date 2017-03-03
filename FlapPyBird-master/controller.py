from __future__ import print_function

import sys
import game.wrapped_flappy_bird as game
import random
from math import sqrt, atan2
from argparse import Action
from tkinter.constants import CURRENT

ACTIONS = 2
FIRST_JUMP = True
LEARNING_RATE = 1
DISCOUNT_FACTOR = 1
DEFAULT_REWARD = 0
QMATRIX = {}

def run():
    game_state = game.GameState()
    flap = 0
#     qMatrix = {}
#     for x in range(-9,11):
#         for y in range(0,51):
#             for z in range(-16,17):
#                 for g in range(-6,7):
#                     state = (x,y,z,g)
#                     actionReward = [[-1,DEFAULT_REWARD],[-1,DEFAULT_REWARD]]
#                     qMatrix[state] = actionReward
#     state = (-9,0,-16,6)
#     actionReward = qMatrix.get(state)
#     actionReward[0][0]=(-9,0,-16,-5)
#     actionReward[0][1]=-1
#     qMatrix[state] = actionReward
#     print(qMatrix[state])
#     print(qMatrix.get(qMatrix.get(state)[0][0]))
    state, reward, terminal = game_state.frame_step(flap)
    currentState = discretizeState(state)
    actionReward = [int(DEFAULT_REWARD),int(DEFAULT_REWARD)]
    QMATRIX[currentState] = actionReward
    currentActionReward = QMATRIX[currentState]
    print(QMATRIX)
    deathCount = 0
    score = 0
    scoreList = []
    while True:
        flap = qStrategy(currentActionReward)
        #flap = randomStrategy()
        #flap = heuristicStrategy(state)
        newState, newReward, terminal = game_state.frame_step(flap)
        newState = discretizeState(newState)
        if(QMATRIX.get(newState) is None):
            actionReward = [int(DEFAULT_REWARD),int(DEFAULT_REWARD)]
            QMATRIX[newState] = actionReward
        currentActionReward[flap] = calcReward(currentActionReward[flap],newReward,newState)
        QMATRIX[currentState] = currentActionReward
        currentState = newState
        currentActionReward = QMATRIX[currentState]
        score+=1
        if(terminal):
            if(len(scoreList)<100):
                scoreList.append(score)
            else:
                scoreList.pop(0)
                scoreList.append(score)
            deathCount+=1
            score = 0
            print("DEATH: ",deathCount," SPD100: ",sum(scoreList)/len(scoreList))
            #print("QMATRIX: ",QMATRIX)
    
def calcReward(currentReward,newReward,newState):
    newActionReward = QMATRIX.get(newState)
    return currentReward + LEARNING_RATE*(newReward+DISCOUNT_FACTOR*getMax(newActionReward)-currentReward)

def getMax(newActionReward):
    if(newActionReward[1]>newActionReward[0]):
        return newActionReward[1]
    return newActionReward[0]

def qStrategy(actionReward):
    notFlap = actionReward[0]
    flap = actionReward[1]
    if(flap>notFlap):
        return 1
    elif(notFlap>flap):
        return 0
    else:
        return randomStrategy()
    
def discretizeState(state):
    player = state['playerRect']
    playerVelY = state['playerVelY']
    birdMid = (player.x,player.y+(player.height/2))
    upperPipeList = state['uPipeRects']
    lowerPipeList = state['lPipeRects']
    discState = [playerVelY]
    for x in range(0,len(upperPipeList)):
        if(player.left<upperPipeList[x].right):
            pipeMid = (upperPipeList[x].right,(upperPipeList[x].bottom+lowerPipeList[x].top)/2)
            if(x!=len(upperPipeList)-1):
                discState.append(distanceBirdToPipeMiddle(birdMid,pipeMid))
            if(x==len(upperPipeList)-1 and upperPipeList[x].right-player.left>279):
                discState.append(0)
            else:
                discState.append(angleBirdToPipeMiddle(birdMid,pipeMid))
    return (discState[0],discState[1],discState[2],discState[3])
    
def distanceBirdToPipeMiddle(birdMid,pipeMid):
    xDistance = pipeMid[0]-birdMid[0]
    yDistance = pipeMid[1]-birdMid[1]
    return int(sqrt((xDistance)**2+(yDistance)**2)/4)

def angleBirdToPipeMiddle(birdMid,pipeMid):
    diffPoint = (pipeMid[0]-birdMid[0],pipeMid[1]-birdMid[1])
    return int(atan2(diffPoint[1],diffPoint[0])*10)   
 
def randomStrategy():
    actionRange = ACTIONS*100
    if(random.randrange(actionRange)>175):
        return 1
    return 0

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
        return 1
    elif(pipeDecrease(nextLowerPipe,nextNextLowerPipe) and earliestExitPoint(player,nextLowerPipe, pipeVelX, nextUpperPipe)):
        return 1
    else:
        return 0

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