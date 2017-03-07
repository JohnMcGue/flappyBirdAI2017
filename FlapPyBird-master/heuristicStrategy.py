class heuristicStrategy:
    def getAction(self,state):
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
