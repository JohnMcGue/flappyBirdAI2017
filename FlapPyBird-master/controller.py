from __future__ import print_function

import game.wrapped_flappy_bird as game
import random
import pickle
from heuristicStrategy import heuristicStrategy
from QLearning import QLearning
import datetime

from math import sqrt, atan2
from time import clock
 
LEARNING_RATE = .8
DISCOUNT_FACTOR = .9
DEFAULT_REWARD = 0
QMATRIX = {}
EP = 0.1
ACTIONS = 2
STRATEGY = QLearning()


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
    while (deathCount < 50000):
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
               EP = EP*.999
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

def test(timer):
    game_state = game.GameState()
    game_state.setFPS(30)
    flap = 0
    state, reward, terminal = game_state.frame_step(flap)
    deathCount = 0
    score = 0
    scoreList = []
    endTime = datetime.datetime.now().time() + datetime.timedelta(minutes=timer)
    while (datetime.datetime.now().time() < endTime):
        flap = STRATEGY.getAction(state)
        state, newReward, terminal = game_state.frame_step(flap)
        if(terminal):
            if(len(scoreList)<100):
                scoreList.append(score)
            else:
                scoreList.pop(0)
                scoreList.append(score)
            deathCount+=1
            score = 0
            print("DEATH: ",deathCount," SPD100: ",sum(scoreList)/len(scoreList))
        else:
            score+=1

def train(timer):
    game_state = game.GameState()
    flap = 0
    state, reward, terminal = game_state.frame_step(flap)
    endTime = datetime.datetime.now().time() + datetime.timedelta(minutes=timer)
    while (datetime.datetime.now().time() < endTime):
        flap = STRATEGY.getAction(state)
        state, newReward, terminal = game_state.frame_step(flap)
        STRATEGY.train(state, newReward, terminal)
    pickle.dump(QMATRIX, open("save.p", "wb" ) )
    
def main():
    global STRATEGY
    print("Q or H?")
    uInput = input()
    if(uInput == "H"):
        STRATEGY = heuristicStrategy()
        uInput = getTime()
        test(uInput)
    elif(uInput == "Q")
        STRATEGY = QLearning()
        print("test or train?")
        if(uInput == "test"):
            QLearning.setEP(0)
            timer = getTime()
            test(timer)
        elif(uInput == "train"):
            timer = getTime()
            train(timer)

def getTime():
    print("how long (minutes)?")
    return input() 

if __name__ == "__main__":
    main()