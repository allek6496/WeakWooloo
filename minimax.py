'''
I didn't want to totally delete calculator.py so I made this
1, 2 and 3 still mean throw duck and reload respectilvely
'''

import sys 

#make a class that stores a single game state
class state:
    def __init__(self, snow1, snow2,
                 ducks1, ducks2,
                 points1, points2, round, prevMove=0, bestMove=0):
        self.snow1 = snow1
        self.snow2 = snow2
        self.ducks1 = ducks1
        self.ducks2 = ducks2
        self.points1 = points1
        self.points2 = points2
        self.round = round
        self.prevMove = prevMove
        self.value = None
        self.bestMove = -1

    #checks if two states are equal
    def __eq__(self, state2):
        try:
            return self.snow1 == state2.snow1 and \
                self.snow2 == state2.snow2 and \
                self.ducks1 == state2.ducks1 and \
                self.ducks2 == state2.ducks2 and \
                self.points1 == state2.points1 and \
                self.points2 == state2.points2 and \
                self.round == state2.round
        except:
            return False

    #puts the variables in a list of consistent formatting
    def parse(self):
        return [self.snow1, self.snow2, self.ducks1, self.ducks2, self.points1, self.points2, self.round, self.value, self.bestMove]

    #returns the possible states the current state can lead to
    def nextStates(self):
        if self.round < 60:
            if self.round%2 == 0:
                nextStates = []
                for move1 in [1, 2, 3]:
                    nextData = [self.snow1, self.snow2, self.ducks1, self.ducks2, self.points1, self.points2, self.round+1, move1]
                    
                    #first player
                    if move1 == 1 and self.snow1 > 0:
                        #if they threw, they have one less snowball
                        nextData[0] -= 1
                        nextStates.append(state(*nextData))
                    elif move1 == 1:
                        nextStates.append(-1)
                    
                    if move1 == 2 and self.ducks1 > 0:
                        #if they ducked, they have one less duck
                        nextData[2] -= 1
                        nextStates.append(state(*nextData))
                    elif move1 == 2:
                        nextStates.append(-1)
                    
                    if move1 == 3 and self.snow1 < 10:
                        #if they reload they have one more snowball
                        nextData[0] += 1
                        nextStates.append(state(*nextData))
                    elif move1 == 3:
                        nextStates.append(-1)
                    
                return nextStates

            else:
                nextStates = []
                for move2 in [1, 2, 3]:
                    nextData = [self.snow1, self.snow2, self.ducks1, self.ducks2, self.points1, self.points2, self.round+1, move2]

                    #second player
                    if move2 == 1 and self.snow2 > 0:
                        nextData[1] -= 1
                        if self.prevMove == 3:
                            nextData[5] += 1
                            if nextData[5] == 3:
                                nextStates.append(-1) #player 2 wins
                                continue
                        nextStates.append(state(*nextData))
                    elif move2 == 1:
                        nextStates.append(1) #cheat, so player 1 wins    

                    if move2 == 2 and self.ducks2 > 0:
                        nextData[3] -= 1
                        nextStates.append(state(*nextData))
                    elif move2 == 2:
                        nextStates.append(1)

                    if move2 == 3 and self.snow2 < 10:
                        nextData[1] += 1
                        if self.prevMove == 1:
                            nextData[4] += 1
                            if nextData[4] == 3:
                                nextStates.append(1) #player 1 wins
                                continue
                        nextStates.append(state(*nextData))
                    elif move2 == 3:
                        nextStates.append(1)

                return nextStates
        else:
            return [0, 0, 0] #it can only be a tie from here

nodes = 0
games = [[] for i in range(61)]

def treeMax(thisState):
    global nodes
    nodes += 1
    global games

    if nodes%100000 == 0:
        print(nodes, "evaluated")

    children = thisState.nextStates()

    child1, child2, child3 = None, None, None

    if children[0] in [-1, 0, 1]:
        child1 = children[0]
    else:
        if children[0] not in games[children[0].round]:
            child1 = treeMin(children[0])
        else:
            for state in games[children[0].round]:
                if state == children[0]:
                    child1 = state.value
                    break

    if children[1] in [-1, 0, 1]:
        child2 = children[1]
    else:
        if children[1] not in games[children[1].round]:
            child2 = treeMin(children[1])
        else:
            for state in games[children[1].round]:
                if state == children[1]:
                    child2 = state.value
                    break

    if children[2] in [-1, 0, 1]:
        child3 = children[2]
    else:
        if children[2] not in games[children[2].round]:
            child3 = treeMin(children[2])
        else:
            for state in games[children[2].round]:
                if state == children[2]:
                    child3 = state.value
                    break

    values = [child1, child2, child3]
    value = max(values)
    bestMove = values.index(value) + 1

    thisState.bestMove = bestMove
    thisState.value = value
    games[thisState.round].append(thisState)

    return value

def treeMin(thisState):
    #same but min instead
    global nodes
    nodes += 1
    global games

    if nodes%100000 == 0:
        print(nodes, "evaluated")

    children = thisState.nextStates()

    child1, child2, child3 = None, None, None

    if children[0] in [-1, 0, 1]:
        child1 = children[0]
    else:
        if children[0] not in games[children[0].round]:
            child1 = treeMax(children[0])
        else:
            for state in games[children[0].round]:
                if state == children[0]:
                    child1 = state.value
                    break

    if children[1] in [-1, 0, 1]:
        child2 = children[1]
    else:
        if children[1] not in games[children[1].round]:
            child2 = treeMax(children[1])
        else:
            for state in games[children[1].round]:
                if state == children[1]:
                    child2 = state.value
                    break

    if children[2] in [-1, 0, 1]:
        child3 = children[2]
    else:
        if children[2] not in games[children[2].round]:
            child3 = treeMax(children[2])
        else:
            for state in games[children[2].round]:
                if state == children[2]:
                    child3 = state.value
                    break

    values = [child1, child2, child3]
    value = min(values)
    bestMove = values.index(value) + 1

    thisState.bestMove = bestMove
    thisState.value = value

    games[thisState.round].append(thisState)

    return value

# children = state(1, 1, 5, 5, 0, 0, 0).nextStates()

# for child in children:
#     print(child.parse())
#     grandChildren = child.nextStates()
#     for grandchild in grandChildren:
#         print('\t', grandchild.parse())

f = open('tree.txt', 'w')

treeMax(state(1, 1, 5, 5, 0, 0, 0))

data = []
for r in range(0, len(games)):
    if len(games[r]) > 0 and r%2 == 0:

        data.append([state.parse() for state in games[r]])

f.write(str(data))

f.close()

# children = state(0, 1, 5, 5, 0, 0, 1).nextStates()

# for child in children:
#     print(child.parse())