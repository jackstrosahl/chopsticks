from math import inf
from networkx import DiGraph, draw
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import queue

def pos_string(position):
    return "".join("".join(str(hand) for hand in player) for player in position)

# Only 2 for now
num_hands = 2
num_players = 2
rollover = 5
start_hand = (1,1)
start_position = tuple(start_hand for _ in range(num_players))

state = (0,start_position,None)
q = queue.Queue()
explored = set()
q.put(state)

graph = DiGraph()
while not q.empty():
    state = q.get()
    move, position, parent = state
    if parent is not None:
        graph.add_edge(parent,position)
    if position in explored:
        continue
    explored.add(position)
    
    cur_player = position[0]
    next_move = move + 1        
    
    def queue_move(new_player,i=0):
        new_position = list(position[1:])
        if i == 0:
            new_position.append(new_player)
        else:
            new_position.append(position[0])
            new_position[i-1] = new_player
        q.put((next_move, tuple(new_position), position))

    sum_fingers = sum(cur_player)

    # Generate all transfers and divisions
    if sum_fingers == 0:
        continue

    min_hand = min(cur_player)
    assert sum_fingers <= (rollover-1)*num_hands
    for fingers in range(1,min(sum_fingers+1,rollover)):
        o_fingers = sum_fingers - fingers
        if o_fingers >= rollover:
            continue
        new_player = tuple(sorted((fingers, o_fingers)))
        if new_player == cur_player or (min_hand > 0 and min(new_player) == 0):
            continue
        queue_move(new_player)

    # Generate all attacks
    for opp_i in range(1,num_players):
        opp_player = position[opp_i]
        for fingers in cur_player:
            if fingers == 0:
                continue
            for opp_hand in range(num_hands):
                new_player = list(opp_player)
                if new_player[opp_hand] == 0:
                    continue
                new_player[opp_hand] = (new_player[opp_hand] + fingers) % rollover
                queue_move(tuple(sorted(new_player)),opp_i)

print(len(explored))
# pos = graphviz_layout(graph, prog="dot")
# draw(graph, pos, with_labels=True, node_size=800)
# plt.show()

best_moves = {}
nm_explored = set()
def negamax(position, player):
    explored_key = (position,player)
    if explored_key in nm_explored:
        return 0
    nm_explored.add(explored_key)
    succs = list(graph.successors(position))
    if len(succs) == 0:
        best_moves[position] = None
        return player
    value = -inf
    best_move = None
    for succ in succs:
        alt = -negamax(succ, -player)
        if alt > value:
            value = alt
            best_move = succ

    best_moves[position] = best_move
    return value

print(negamax(start_position, 1))
print(best_moves)