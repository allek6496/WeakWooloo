# This creates the array object that contains the min-max tree

# I think a recursive approach won't work because of stack overflows, so here's a basic iterative approach

tree = [] 
'''
If this array gets bigger than 536,870,912 elements it'll break, but I don't think that will happen
since there are much less than 3^30 possible game states. If something really weird happens and it
does break, we can always just write to a file.

The format of this array is very important. It can be lots of different things, but here's my idea:

Assume a throw is 0, a reload is 1 and a duck is 2 (totally arbitrary).

tree[0][1][2][1] should be the state after player 1 threw and player 2 relaoded then 
                                           player 1 ducked and player 2 reloaded

That "state" should contain a list of where the game could go next and whether or not someone wins
'''
    
explore = []
# This stores which states to look at next

for round in range(60):

    for state in explore:
        # Evaluate another case on this round number, marking if it's winning, losing or can be continued
        pass # This is just here so there's no error

    print("Evaluated round", str(round), "with", len(explore), "game states")

'''
At this point, there's a tree of game states, and whether or not someone winned there

Now, we need a second program that will go through those game states and find the optimal move.

I think it should work backwords, so it starts at round 29 and finds the optimal move to either
win or tie. Then it goes through each possible state at round 28, and so on until round 1. This
is the hardest part imo and I don't really know what to do for it
'''
