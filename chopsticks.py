from collections import OrderedDict, defaultdict
import queue

# Only 2 for now
num_hands = 2
num_players = 2
rollover = 5
start_hand = (1,1)

state = (0,*(start_hand for _ in range(num_players)))
q = queue.Queue()
explored = set()
q.put(state)
position_set = set()

while not q.empty():
    state = q.get()
    move, *players = state
    turn = move % num_players
    position = (turn, *players)
    alt_position = tuple(players if turn == 0 else reversed(players))
    if alt_position in explored:
        continue

    cur_player = players[turn]
    next_move = move + 1
    # Generate all transfers and divisions
    sum_fingers = sum(cur_player)

    position_set.add(alt_position)
    explored.add(alt_position)

    if sum_fingers == 0:
        continue

    min_hand = min(cur_player)
    assert sum_fingers <= (rollover-1)*num_hands
    for fingers in range(1,min(sum_fingers+1,rollover)):
        o_fingers = sum_fingers - fingers
        if o_fingers >= rollover:
            continue
        new_players = players[:]
        new_player = tuple(sorted((fingers, o_fingers)))
        if new_player == cur_player or (min_hand > 0 and min(new_player) == 0):
            continue
        new_players[turn] = new_player
        q.put((next_move,*new_players))
    # Generate all attacks
    for opp_i in range(num_players):
        if opp_i == turn:
            continue
        opp_player = players[opp_i]
        for fingers in cur_player:
            if fingers == 0:
                continue
            for opp_hand in range(num_hands):
                new_player = list(opp_player)
                if new_player[opp_hand] == 0:
                    continue
                new_player[opp_hand] = (new_player[opp_hand] + fingers) % rollover
                new_players = players[:]
                new_players[opp_i] = tuple(sorted(new_player))
                q.put((next_move,*new_players))

print(len(explored))