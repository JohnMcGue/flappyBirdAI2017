import pickle
import random

LEARNING_RATE = 1
DISCOUNT_FACTOR = .99
DEFAULT_REWARD = 0
EP = .01
FLOOREP = .01
DEATHS_EP_REDUCTION = 3
QMATRIX = {}
ACTIONS = 2
CSTATE = None
TERMINAL = False
DEATHCOUNT = 0

class qLearningStrategy:
    def setFloorEP(self,value):
        global FLOOREP
        FLOOREP = value
    
    def setLearningRate(self,value):
        global LEARNING_RATE
        LEARNING_RATE = value
        
    def setDiscount(self,value):
        global DISCOUNT_FACTOR
        DISCOUNT_FACTOR = value
        
    def setDefaultReward(self,value):
        global DEFAULT_REWARD
        DEFAULT_REWARD = value
    
    def printQMATRIX(self):
        global QMATRIX
        print(QMATRIX)
    
    def __init__(self):
        global QMATRIX
        try:
            QMATRIX = pickle.load(open("save.p", "rb"))
        except (OSError, IOError, EOFError) as e:
            print("No saved matrix: ",e)
    
    def getAction(self,state):
        global TERMINAL
        global EP
        global QMATRIX
        if(TERMINAL):
            TERMINAL = False
            return 0
        state = discretizeState(state)
        actionReward = QMATRIX[state]
        notFlap = actionReward[0]
        flap = actionReward[1]
        randomNumber = random.randrange(0,100)/100
        if(EP > randomNumber):
            return randomStrategy()
        if(flap>notFlap):
            return 1
        elif(notFlap>flap):
            return 0
        else:
            return randomStrategy()
    
    def setEP(self,value):
        global EP
        EP = value
    
    def train(self, state, newReward, terminal, flap):
        global CSTATE
        global TERMINAL
        global DEATHCOUNT
        global EP
        global FLOOREP
        global DEATHS_EP_REDUCTION
        TERMINAL = terminal
        state = discretizeState(state)
        if(CSTATE is None):
            CSTATE = state
        if(TERMINAL):
            QMATRIX[CSTATE][flap] = newReward
            DEATHCOUNT += 1
            if DEATHCOUNT % DEATHS_EP_REDUCTION == 0 and EP>FLOOREP:
               EP = EP*.999
        else:
            QMATRIX[CSTATE][flap] = updateReward(flap, state, newReward)
            CSTATE = state
            
    def cleanUp(self):
        global QMATRIX
        pickle.dump(QMATRIX, open("save.p", "wb" ) )
        
    def deleteSave(self):
        pickle.dump({}, open("save.p", "wb" ) )
            
def updateReward(flap, newState, newReward):
    global QMATRIX
    global CSTATE
    oldReward = QMATRIX[CSTATE][flap]
    return oldReward + LEARNING_RATE*(newReward+DISCOUNT_FACTOR*getMax(newState)-oldReward)

def getMax(newState):
    global QMATRIX
    newActionReward = QMATRIX[newState]
    if(newActionReward[1]>newActionReward[0]):
        return newActionReward[1]
    return newActionReward[0]

def randomStrategy():
    global ACTIONS
    return random.randrange(ACTIONS)

def discretizeState(state):
    player = state['playerRect']
    lowerPipeList = state['lPipeRects']
    discState = []
    for x in range(0,len(lowerPipeList)):
        if(player.left<lowerPipeList[x].right):
            if(x!=len(lowerPipeList)-1):
                discState.append(lowerPipeList[x].top-player.bottom)
    stateSet = (discState[0])
    initQMATRIX(stateSet)
    return stateSet
    
def initQMATRIX(state):
    global QMATRIX
    if(QMATRIX.get(state) is None):
        QMATRIX[state] = [DEFAULT_REWARD,DEFAULT_REWARD]