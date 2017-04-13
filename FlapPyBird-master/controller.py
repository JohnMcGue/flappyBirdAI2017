from __future__ import print_function

import game.wrapped_flappy_bird as game
from heuristicStrategy import heuristicStrategy
from QLearning import qLearningStrategy
import datetime
import pickle

STRATEGY = None
GAME_STATE = game.GameState()

def test(timer):
    STRATEGY.setEP(0)
    STRATEGY.printQMATRIX()
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    score = 0
    scoreList = []
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=int(timer))
    while (datetime.datetime.now().time() < endTime.time()):
        flap = STRATEGY.getAction(state)
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        if(terminal):
            scoreList.append(score)
            score = 0
        else:
            score+=1
    avgScore = "infinity"
    if(len(scoreList)>0):
        avgScore = sum(scoreList)/len(scoreList)
    print(" AVG SCORE: ",avgScore)
    return len(scoreList),avgScore

def train(timer):
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=int(timer))
    print(endTime)
    iterations = 0
    while (datetime.datetime.now() < endTime):
        flap = STRATEGY.getAction(state)
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        STRATEGY.train(state, newReward, terminal, flap)
        if(terminal):
            iterations = iterations + 1
    STRATEGY.cleanUp()
    print(iterations)
    
def trainIt():
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    counter = 0
    while (counter < 200):
        flap = STRATEGY.getAction(state)
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        STRATEGY.train(state, newReward, terminal, flap)
        if(terminal):
            counter = counter + 1
    flap = STRATEGY.getAction(state)
    state, newReward, terminal = GAME_STATE.frame_step(flap)
    STRATEGY.train(state, newReward, terminal, flap)
    STRATEGY.cleanUp()
    
def testIt():
    global STRATEGY
    STRATEGY.setEP(0)
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    score = 0
    scoreList = []
    counter = 0
    while (counter<100 and score<75000):
        flap = STRATEGY.getAction(state)
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        if(terminal):
            scoreList.append(score)
            score = 0
            counter = counter + 1
        else:
            score+=1
        print(score)
    avgScore = 0
    if(len(scoreList)>0):
        avgScore = sum(scoreList)/len(scoreList)
    if(score>75000):
        avgScore = 0
    print(" AVG SCORE: ",avgScore)
    return avgScore

def main():
    global STRATEGY
    global GAME_STATE
    print("Q or H?")
    uInput = input()
    if(uInput == "H"):
        STRATEGY = heuristicStrategy()
        GAME_STATE.setFPS(30)
        uInput = getTime()
        test(uInput)
    elif(uInput == "Q"):
        STRATEGY = qLearningStrategy()
        print("test or train?")
        uInput = input()
        if(uInput == "test"):
            GAME_STATE.setFPS(30000)
            timer = getTime()
            test(timer)
        elif(uInput == "train"):
            timer = getTime()
            train(timer)
    elif(uInput == "D"):
        STRATEGY = qLearningStrategy()
        STRATEGY.deleteSave()
        #print("learning rate?")
        #uInput = input()
        #learningRate = uInput
        #print("discount factor?")
        #uInput = input()
        #discountFactor = uInput
    elif(uInput == "T"):
        STRATEGY = qLearningStrategy()
        testtest()

def testtest():
    global STRATEGY
    csvString = ""
    high = .99
    low = .01
    middle = .5
    for i in range(0,9):
        if(i==0):
            STRATEGY.setDiscount(low)
            STRATEGY.setLearningRate(low)
        if(i==1):
            STRATEGY.setLearningRate(middle)
        if(i==2):
            STRATEGY.setLearningRate(high)
        if(i==3):
            STRATEGY.setDiscount(middle)
            STRATEGY.setLearningRate(low)
        if(i==4):
            STRATEGY.setLearningRate(middle)
        if(i==5):
            STRATEGY.setLearningRate(high)
        if(i==6):
            STRATEGY.setDiscount(high)
            STRATEGY.setLearningRate(low)
        if(i==7):
            STRATEGY.setLearningRate(middle)
        if(i==8):
            STRATEGY.setLearningRate(high)
        for j in range(0,2):
            if(j==0):
                STRATEGY.setEP(.01)
                STRATEGY.setFloorEP(.01)
            if(j==1):
                STRATEGY.setEP(.1)
                STRATEGY.setFloorEP(.1)
            STRATEGY.setDiscount(.99)
            STRATEGY.setLearningRate(.01)
            csvString += "LR="+str(STRATEGY.getLearningRate())+",DF="+str(STRATEGY.getDiscount())+",EP="+str(STRATEGY.getEP())+"\n"+"Iterations,Score \n 0,48.98 \n"
            test = 1
            iterations = 0
            while(test>0 and iterations < 15000):
                iterations = iterations + 200
                print(iterations)
                trainIt()
                test = testIt()
                csvString += str(iterations)+","+str(test)+"\n"
        
    text_file = open("data.csv", "w")
    text_file.write(csvString)
    text_file.close()

def getTime():
    print("how long (minutes)?")
    return input() 

if __name__ == "__main__":
    main()