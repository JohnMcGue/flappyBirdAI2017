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
    

def getTimeFromUser():
    print("how long (minutes)?")
    return input() 

    
def trainIt():
    global GAME_STATE
    global STRATEGY
    STRATEGY.setEP(0.01)
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    flap = STRATEGY.getAction(STRATEGY.discretize(state))
    counter = 0
    while (counter < 200):
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        newFlap = STRATEGY.train(state, newReward, terminal, flap)
        flap = newFlap
        if(terminal):
            counter = counter + 1
    STRATEGY.cleanUp()
    
def testIt():
    global STRATEGY
    global GAME_STATE
    STRATEGY.setEP(0)
    flap = 0
    state, reward, terminal = GAME_STATE.frame_step(flap)
    score = 0
    scoreList = []
    counter = 0
    while (counter<100 and score<75000):
        flap = STRATEGY.getAction(STRATEGY.discretize(state))
        state, newReward, terminal = GAME_STATE.frame_step(flap)
        if(terminal):
            scoreList.append(score)
            score = 0
            counter = counter + 1
        else:
            score = score + 1
    avgScore = 0
    if(len(scoreList)>0):
        avgScore = sum(scoreList)/len(scoreList)
    if(score>=75000):
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
            timer = 1
            test(timer)
        elif(uInput == "train"):
            timer = 10
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
    STRATEGY.setDiscount(.99)
    STRATEGY.setLearningRate(.01)
    csvString += "LR="+str(STRATEGY.getLearningRate())+",DF="+str(STRATEGY.getDiscount())+",EP="+str(STRATEGY.getEP())+"\n"+"Iterations,Score \n 0,48.98 \n"
    test = 1
    iterations = 0
    while(test>0 and iterations < 10000):
        print(iterations)
        iterations = iterations + 200
        trainIt()
        test = testIt()
        csvString += str(iterations)+","+str(test)+"\n"
    #STRATEGY.deleteSave()
    text_file = open("data.csv", "w")
    text_file.write(csvString)
    text_file.close()

if __name__ == "__main__":
    main()
    
    