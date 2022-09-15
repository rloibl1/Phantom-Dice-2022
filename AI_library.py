import numpy as np

# =====================
# AI Enabling Functions
# =====================


# Helper Function for Executing Actions
def dice_removal(board_state, column, roll, player):
    # Keep Track of Dice Remaining
    remaining_dice = list()
    removal = False
    for row in range(board_state.shape[2]):
        if board_state[player, row, column] == roll:
            # Remove Die From Opponent
            board_state[player, row, column] = 0
            removal = True
        else:
            # Add to Tracking List
            remaining_dice.append(board_state[player, row, column])
    # Re-Arrange Dice
    if removal:
        for i in range(board_state.shape[2]):
            try:
                board_state[player, -(i + 1), column] = remaining_dice.pop()
            except IndexError:
                board_state[player, -(i + 1), column] = 0
    return board_state


# Player Picks Column and the Die is added to the First Available Spot
# Determine Row for the Die and then Place the Die (Lowest Row First)
def execute_action(agent, board_state, action, roll):
    # print(board_state)
    for row in range(board_state.shape[2]):
        if board_state[agent, -(row+1), action] == 0:
            # Place the Die for Player
            board_state[agent, -(row+1), action] = roll
            # Remove Opponents Dice if they are the Same
            board_state = dice_removal(board_state=board_state, column=action, roll=roll, player=int(not bool(agent)))
            return board_state
    # Return that the Move was Invalid (Column was Full)
    return False


# Returns a one hot array [0, 0, 0] where a 1 means the action is valid
def possible_actions(agent, board_state):
    # Start by assuming all actions are invalid
    actions = np.zeros(3, dtype=np.int8)
    for col in range(board_state.shape[1]):
        for row in range(board_state.shape[2]):
            value = board_state[agent, row, col]
            if value == 0:
                actions[col] = 1
    return actions


# Calculates the value of a given board state
# Takes a board state as an input
# Returns Player Score - Opponent Score
# Player is the agent - used to calculate the delta
def calculate_utility(agent, board_state):
    player_scores = np.zeros(2, dtype=np.int16)
    # Calc score for both players
    for player in range(board_state.shape[0]):
        # Calculate Score for Each Column
        for col in range(board_state.shape[1]):
            single_list, double_list, triple_list = ([] for i in range(3))
            for row in range(board_state.shape[2]):
                value = board_state[player, row, col]
                if value in single_list:
                    double_list.append(value)
                    single_list.remove(value)
                elif value in double_list:
                    triple_list.append(value)
                    double_list.remove(value)
                else:
                    single_list.append(value)
            # Calculate Score Using Single, Double, Triple Lists
            player_scores[player] += np.sum(single_list) + (np.sum(double_list) * 4) + (np.sum(triple_list) * 9)
    if agent == 0:
        return int(player_scores[0] - player_scores[1])
    else:
        return int(player_scores[1] - player_scores[0])


# Calculates the average value of an action for all possible outcomes (dice rolls 1-6)
def calculate_expected_value(agent, board_state, action):
    avg_utility = 0
    for dice_roll in range(1, 7):
        # Apply Move
        new_state = execute_action(agent=agent, board_state=board_state.copy(), action=action, roll=dice_roll)
        avg_utility += calculate_utility(agent=agent, board_state=new_state)
    return avg_utility / 6


# Determines if the Game has ended
def endgame_check(board_state):
    for i in range(board_state.shape[0]):
        for j in range(board_state.shape[1]):
            for k in range(board_state.shape[2]):
                if board_state[i, j, k] == 0:
                    return False
    return True
