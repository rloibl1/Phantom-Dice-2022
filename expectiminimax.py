# Stochastic Minimax Algorithm
from AI_library import *
from game_library import *


def is_max(agent):
    if agent == 0:
        return True
    else:
        return False


def is_min(agent):
    if agent == 2:
        return True
    else:
        return False


def is_chance(agent):
    if agent % 2 != 0:
        return True
    else:
        return False


def expectiminimax(agent, board_state, depth):
    # Return Condition - Game has ended or the depth cutoff was reached
    if endgame_check(board_state=board_state) or depth == 0:
        return calculate_utility(agent=agent, board_state=board_state)
    # Max Agent
    elif is_max(agent=agent):
        return None
    # Min Agent
    elif is_min(agent=agent):
        return None
    elif is_chance(agent=agent):
        return calculate_expected_value(agent=agent)

    # Change Turn
    _agent = int(not(bool(agent)))

    # Get possible actions at this state node
    actions = possible_actions(agent=_agent, board_state=board_state)

    # Explore all possible actions
    for i, action in enumerate(actions):
        if action == 1:
            utility = expectiminimax(agent=_agent,
                                     board_state=execute_action(agent=_agent, board_state=board_state, action=i, ),
                                     depth=depth-1)


new_game = KnuckleBones()
agent = 1

# expectiminimax()

print(is_chance(4))
