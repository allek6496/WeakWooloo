def nextMoves(state, player):
    if player == 0:
        #good guy
        snow = state[1]
        ducks = state[3]

        moves = []

        if snow > 0:
            #throw
            moves.append(1)
        
        if ducks < 5:
            #duck
            moves.append(2)
        
        if snow < 10:
            #reload
            moves.append(3)

        return moves
    else:
        #bad guy
        snow = state[2]
        ducks = state[4]

        moves = []

        if snow > 0:
            #throw
            moves.append(1)
        
        if ducks < 5:
            #duck
            moves.append(2)
        
        if snow < 10:
            #reload
            moves.append(3)

        return moves

def nextState(move1, move2, state):
    nState = state[:]
    nState[0] += 1
    
    if move1 == 1:
        nState[1] -= 1
    if move1 == 2:
        nState[3] += 1
    if move1 == 3:
        nState[1] += 1

    if move2 == 1:
        nState[2] -= 1
    if move2 == 2:
        nState[4] += 1
    if move2 == 3:
        nState[2] += 1

    if move1 == 1 and move2 == 3:
        nState[5] += 1
    if move2 == 1 and move1 == 3:
        nState[6] += 1

    return nState

def get(state):
    global tree
    r = state[0]

    while r >= len(tree):
        tree.append([])

    # print(tree)
    for s in tree[r]:
        if s[:7] == state or s == state:
            # print("worked")
            return s[-1]
    
    return False

def add(state):
    global tree, nodes
    r = state[0]
    
    if not get(state):
        nodes += 1
        if nodes%frequency == 0:
            print(nodes/frequency, "*", frequency, "nodes")
        
        tree[r].append(state)

def maxWool(state):
    global tree, maxTurns, nodes

    if state[5] == 3:
        return 1
    elif state[6] == 3:
        return -1
    elif state[0] >= maxTurns:
        if state[5] > state[6]:
            return 1
        elif state[6] > state[5]:
            return -1
        else:
            return 0

    prev = get(state)
    if prev:
        return prev[0]
    
    moves = nextMoves(state, 0)
    responses = []

    for move in moves:
        responses.append(miniWool(move, state[:]))
        # print("A", state, move, responses[-1])

    best = max(responses)

    value = 0
    if any(resp > 0 for resp in responses):
        value = sum([resp for resp in responses if resp > 0])
    elif any(resp == 0 for resp in responses):
        value = 0
    else:
        value = sum(responses)

    #either this /\  way to get value or this \/ way

    # value = sum(responses)

    state.append([value, moves[responses.index(best)]])
    add(state)

    return value

def miniWool(prevMove, state):
    global tree, nodes

    moves = nextMoves(state, 1)

    responses = []

    for move in moves:
        responses.append(maxWool(nextState(prevMove, move, state)))
        # print("B", state, move, responses[-1])
    
    value = 0
    if any(resp < 0 for resp in responses):
        value = sum([resp for resp in responses if resp < 0])
    elif any(resp == 0 for resp in responses):
        value = 0
    else:
        value = sum(responses)

    #either this /\ or this \/

    #value = sum(responses)

    return value

maxTurns = 6
frequency = 1000
tree = [[]]
nodes = 0

'''
round
snow1
snow2
ducksUsed1
ducksUsed2
points1
points2
'''
maxWool([0, 1, 1, 0, 0, 0, 0])

f = open("horn.txt", 'w')

f.write(str(tree))

f.close()
