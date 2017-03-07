from __future__ import print_function

import game.wrapped_flappy_bird as game
import random
import pickle
from decimal import *

from math import sqrt, atan2
 
LEARNING_RATE = .8
DISCOUNT_FACTOR = .9
DEFAULT_REWARD = 0
QMATRIX = {}
EP = 0.1
ACTIONS = 2


def run():
    game_state = game.GameState()
    flap = 0
    global QMATRIX
    global EP
    try:
        QMATRIX = pickle.load(open("save.p", "rb"))
    except (OSError, IOError, EOFError) as e:
        print("No saved matrix: ",e)
    print(QMATRIX)
    state, reward, terminal = game_state.frame_step(flap)
    currentState = discretizeState(state)
    initQMATRIX(currentState)
    deathCount = 0
    score = 0
    scoreList = []
    while (deathCount < 100000):
        #flap= heuristicStrategy(state)
        flap = qStrategy(currentState)
        state, newReward, terminal = game_state.frame_step(flap)
        if(terminal):
            QMATRIX[currentState][flap] = newReward
            flap = 0
            state, reward, terminal = game_state.frame_step(flap)
            currentState = discretizeState(state)
            initQMATRIX(currentState)
            if deathCount % 3 == 0 and EP>.1:
               EP = Decimal(EP*Decimal(.999))
            if(len(scoreList)<100):
                scoreList.append(score)
            else:
                scoreList.pop(0)
                scoreList.append(score)
            deathCount+=1
            score = 0
            #print("DEATH: ",deathCount," SPD100: ",sum(scoreList)/len(scoreList), "EP: ",EP)
            #pickle.dump(QMATRIX, open("save.p", "wb" ) )
            #print("QMATRIX: ",QMATRIX)
        else:
            newDiscState = discretizeState(state)
            initQMATRIX(newDiscState)
            QMATRIX[currentState][flap] = updateReward(currentState, flap, newDiscState, newReward)
            currentState = newDiscState
            score+=1
            #print("QMATRIX: ",QMATRIX)
    pickle.dump(QMATRIX, open("save.p", "wb" ) )
    game_state.setFPS(30)
    state, reward, terminal = game_state.frame_step(flap)
    currentState = discretizeState(state)
    initQMATRIX(currentState)
    deathCount = 0
    score = 0
    scoreList = []
    EP = 0
    while (deathCount < 10):
        flap = qStrategy(currentState)
        state, newReward, terminal = game_state.frame_step(flap)
        if(terminal):
            flap = 0
            state, reward, terminal = game_state.frame_step(flap)
            currentState = discretizeState(state)
            initQMATRIX(currentState)
            if(len(scoreList)<100):
                scoreList.append(score)
            else:
                scoreList.pop(0)
                scoreList.append(score)
            deathCount+=1
            score = 0
            print("DEATH: ",deathCount," SPD100: ",sum(scoreList)/len(scoreList), "EP: ",EP)
            #print("QMATRIX: ",QMATRIX)
        else:
            newDiscState = discretizeState(state)
            initQMATRIX(newDiscState)
            currentState = newDiscState
            score+=1
    print(QMATRIX)
    
    
def updateReward(currentState, flap, newState, newReward):
    oldReward = QMATRIX[currentState][flap]
    return oldReward + LEARNING_RATE*(newReward+DISCOUNT_FACTOR*getMax(newState)-oldReward)

def initQMATRIX(state):
    if(QMATRIX.get(state) is None):
        QMATRIX[state] = [DEFAULT_REWARD,DEFAULT_REWARD]

def getMax(newState):
    newActionReward = QMATRIX[newState]
    if(newActionReward[1]>newActionReward[0]):
        return newActionReward[1]
    return newActionReward[0]

def qStrategy(currentState):
    actionReward = QMATRIX[currentState]
    global EP
    randomNumber = random.randrange(0,100)/100
    if( EP > randomNumber):
        return randomStrategy()
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
    discState = []
    #discState = [playerVelY]
    for x in range(0,len(upperPipeList)):
        if(player.left<upperPipeList[x].right):
            pipeMid = (upperPipeList[x].right,(upperPipeList[x].bottom+lowerPipeList[x].top)/2)
            if(x!=len(upperPipeList)-1):
                discState.append((pipeMid[0]-birdMid[0])/4)
                discState.append((pipeMid[1]-birdMid[1]))
                #discState.append(distanceBirdToPipeMiddle(birdMid,pipeMid))
            #if(x==len(upperPipeList)-1 and upperPipeList[x].right-player.left>279):
             #   discState.append(0)
            #else:
             #   discState.append(angleBirdToPipeMiddle(birdMid,pipeMid))
    return (discState[0],discState[1])
    #return (discState[0],discState[1],discState[2],discState[3])
    
def distanceBirdToPipeMiddle(birdMid,pipeMid):
    xDistance = pipeMid[0]-birdMid[0]
    yDistance = pipeMid[1]-birdMid[1]
    return int(sqrt((xDistance)**2+(yDistance)**2)/4)

def angleBirdToPipeMiddle(birdMid,pipeMid):
    diffPoint = (pipeMid[0]-birdMid[0],pipeMid[1]-birdMid[1])
    return int(atan2(diffPoint[1],diffPoint[0])*10)   
 
def randomStrategy():
    actionRange = ACTIONS*100
    if(random.randrange(actionRange)>100):
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
    getcontext().prec = 6
    run()

if __name__ == "__main__":
    main()