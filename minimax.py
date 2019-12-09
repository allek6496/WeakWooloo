'''
I didn't want to totally delete calculator.py so I made this

1, 2 and 3 still mean throw duck and reload respectilvely
'''

import sys 

sys.setrecursionlimit(10**6) 

#make a class that stores a single game state
class state:
    def __init__(self, snow1, snow2,
                 ducks1, ducks2,
                 points1, points2, round, prevMove=0):
        self.snow1 = snow1
        self.snow2 = snow2
        self.ducks1 = ducks1
        self.ducks2 = ducks2
        self.points1 = points1
        self.points2 = points2
        self.round = round
        self.prevMove = prevMove
        self.value = None

    #checks if two states are equal
    def isEqual(self, state2):
        return self.snow1 == state2.snow1 and \
               self.snow2 == state2.snow2 and \
               self.ducks1 == state2.ducks1 and \
               self.ducks2 == state2.ducks2 and \
               self.points1 == state2.points1 and \
               self.points2 == state2.points2 and \
               self.round == state2.round

    #returns the possible states the current state can lead to
    def nextStates(self):
        if self.round < 30:
            if self.round%2 == 0:
                nextStates = []
                for move1 in [1, 2, 3]:
                    nextData = [self.snow1, self.snow2, self.ducks1, self.ducks2, self.points1, self.points2, self.round+1, move1]
                    
                    #first player
                    if move1 == 1 and self.snow1 > 0:
                        #if they threw, they have one less snowball and if the other reloads, one more point
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

def treeMax(thisState):
    global nodes
    nodes += 1

    if nodes%100000 == 0:
        print(nodes, "evaluated")

    children = thisState.nextStates()

    if children[0] in [-1, 0, 1]:
        child1 = [children[0], [], [], [], 0, children[0]]
    else:
        child1 = treeMin(children[0])

    if children[1] in [-1, 0, 1]:
        child2 = [children[1], [], [], [], 0, children[1]]
    else:
        child2 = treeMin(children[1])

    if children[2] in [-1, 0, 1]:
        child3 = [children[2], [], [], [], 0, children[2]]
    else:
        child3 = treeMin(children[2])

    values = [child[-1] for child in [child1, child2, child3]]
    value = max(values)
    bestMove = values.index(value) + 1

    return [child1, child2, child3, bestMove, value]

def treeMin(thisState):
    #same but min instead
    global nodes
    nodes += 1

    if nodes%100000 == 0:
        print(nodes, "evaluated")

    children = thisState.nextStates()

    if children[0] in [-1, 0, 1]:
        child1 = [children[0], [], [], [], 0, children[0]]
    else:
        child1 = treeMax(children[0])

    if children[1] in [-1, 0, 1]:
        child2 = [children[1], [], [], [], 0, children[1]]
    else:
        child2 = treeMax(children[1])

    if children[2] in [-1, 0, 1]:
        child3 = [children[2], [], [], [], 0, children[2]]
    else:
        child3 = treeMax(children[2])

    values = [child[-1] for child in [child1, child2, child3]]
    value = min(values)
    bestMove = values.index(value) + 1

    return [child1, child2, child3, bestMove, value]

f = open('tree.txt', 'w')

f.write(str(treeMax(state(1, 1, 5, 5, 0, 0, 0))), buffer=10**10)

f.close()

# stack = [state(1, 1, 5, 5, 0, 0, 0)] #last in first out stack of things to investigate
# history = stack[:] #put each state in here so that you can check if new states are unique
# parents = [] #this will fill up with the whole tree
# path = []

# r = 0
# while len(stack) != 0:
#     current = stack.pop(-1)
#     if current in [0, 1, -1]:
#         path[-1].append(current)

#         if stack[-1].round > r:
#             #evaluate the parent
#             parent = parents[-1]
#             if (r-1) % 2 == 0:
#                 parent[0].bestMove = parent[1:].index(max(parent[1:]))
#             else:
#                 parent[0].bestMove = parent[1:].index(min(parent[1:]))

#     else:
#         r += 1
#         children = current.nextStates()
#         path[-1].append(current)
#         for child in children:
#             if len(filter(lambda state: state.isEqual(child), history)) == 0:
#                 stack.append(child)
#                 history.append(child)
