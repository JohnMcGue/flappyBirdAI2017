from __future__ import print_function

import game.wrapped_flappy_bird as game
from heuristicStrategy import heuristicStrategy
from QLearning import qLearningStrategy
import datetime

STRATEGY = None
GAME_STATE = game.GameState()

def test(timer):
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    score = 0
    scoreList = []
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=int(timer))
    while (datetime.datetime.now().time() < endTime.time()):
        flap = STRATEGY.getAction(STRATEGY.discretize(state))
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        if(terminal):
            scoreList.append(score)
            score = 0
        else:
            score+=1
    avgScore = "infinity"
    if(len(scoreList)>0):
        avgScore = sum(scoreList)/len(scoreList)
    print("DEATHS: ",len(scoreList)," AVG SCORE: ",avgScore)
    return len(scoreList),avgScore

def train(timer):
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=int(timer))
    print(endTime)
    flap = STRATEGY.getAction(STRATEGY.discretize(state))
    while (datetime.datetime.now() < endTime):
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        newFlap = STRATEGY.train(state, newReward, terminal, flap)
        flap = newFlap
    STRATEGY.cleanUp()
    
def main():
    global STRATEGY
    global GAME_STATE
    print("Q or H?")
    uInput = input()
    if(uInput == "H"):
        STRATEGY = heuristicStrategy()
        GAME_STATE.setFPS(30)
        uInput = getTimeFromUser()
        test(uInput)
    elif(uInput == "Q"):
        STRATEGY = qLearningStrategy()
        print("test or train?")
        uInput = input()
        if(uInput == "test"):
            STRATEGY.printQMATRIX()
            GAME_STATE.setFPS(30)
            STRATEGY.setEP(0)
            timer = getTimeFromUser()
            test(timer)
        elif(uInput == "train"):
            timer = getTimeFromUser()
            train(timer)
    elif(uInput == "D"):
        STRATEGY = qLearningStrategy()
        STRATEGY.deleteSave()
        print('learning rate?')
        uInput = input()
        learningRate = uInput
        print('discount factor?')
        uInput = input()
        discountFactor = uInput
        runExperiment(learningRate, discountFactor)

def runExperiment(learningRate, discountFactor):
    STRATEGY.setLearningRate(learningRate)
    STRATEGY.setDiscount(discountFactor)
    

def getTimeFromUser():
    print("how long (minutes)?")
    return input() 

if __name__ == "__main__":
    main()
    
    