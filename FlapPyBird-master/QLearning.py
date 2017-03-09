import pickle
import random

LEARNING_RATE = .8#.8
DISCOUNT_FACTOR = .9#1
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
        #print(QMATRIX)
    
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
        defaultReturn = 0
        if(flap>notFlap):
            defaultReturn = 1
        elif(notFlap>flap):
            defaultReturn = 0
        else:
            #print("equal")
            return randomStrategy()
        randomNumber = random.randrange(0,100)/100
        if(EP > randomNumber):
            if(defaultReturn == 1):
                return 0
            else:
                return 1
        else:
            return defaultReturn
            #return randomStrategy()
    
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
    #playerVelY = state['playerVelY']
    birdMid = (player.x,player.y+(player.height/2))
    upperPipeList = state['uPipeRects']
    lowerPipeList = state['lPipeRects']
    discState = []
    #discState = [playerVelY]
    for x in range(0,len(upperPipeList)):
        if(player.left<upperPipeList[x].right):
            pipeMid = (upperPipeList[x].right,(upperPipeList[x].bottom+lowerPipeList[x].top)/2)
            if(x!=len(upperPipeList)-1):
                discState.append(lowerPipeList[x].top-player.bottom)
                #discState.append((pipeMid[0]-birdMid[0])/4)
                #discState.append((pipeMid[1]-birdMid[1]))
                #discState.append(distanceBirdToPipeMiddle(birdMid,pipeMid))
            #if(x==len(upperPipeList)-1 and upperPipeList[x].right-player.left>279):
             #   discState.append(0)
            #else:
             #   discState.append(angleBirdToPipeMiddle(birdMid,pipeMid))
    #stateSet = (discState[0],discState[1])
    stateSet = (discState[0])
    initQMATRIX(stateSet)
    return stateSet
    #return (discState[0],discState[1],discState[2],discState[3])
    
def initQMATRIX(state):
    global QMATRIX
    if(QMATRIX.get(state) is None):
        QMATRIX[state] = [DEFAULT_REWARD,DEFAULT_REWARD]