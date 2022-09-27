# Stochastic Minimax Algorithm
from AI_library import *
from game_library import *


class MinimaxAgent:
    def __init__(self, eval_agent, max_depth):
        self.eval_agent = eval_agent
        self.max_depth = max_depth

    # Chance Nodes
    def chance_node(self, agent, board_state, action, depth):
        avg_utility = 0
        for dice_roll in range(1, 7):
            avg_utility += self.expectiminimax(agent=int(not agent),
                                               board_state=execute_action(agent=agent,
                                                                          board_state=board_state.copy(),
                                                                          action=action,
                                                                          roll=dice_roll),
                                               depth=depth - 1)
        return avg_utility / 6

    # Minimum and Maximum Nodes - Computes value for a given board state
    def expectiminimax(self, agent, board_state, depth):
        # Return Condition - Game has ended or the depth cutoff was reached
        if endgame_check(board_state=board_state) or depth == 0:
            return calculate_utility(agent=self.eval_agent, board_state=board_state)

        # Get possible actions at this state node
        actions = possible_actions(agent=agent, board_state=board_state)

        # Create List of the Valid Actions
        action_list = list()
        for i, a in np.ndenumerate(actions):
            if a == 1:
                action_list.append(i[0])

        # Minimizer (0)
        if agent == 0:
            # Array to hold utility for all actions
            action_values = np.full((3, ), 1000)
            # Explore all possible actions
            for action in action_list:
                action_values[action] = self.chance_node(agent=agent,
                                                         board_state=board_state.copy(),
                                                         action=action,
                                                         depth=depth)
            return np.min(action_values)
        # Maximizer (1)
        else:
            # Array to hold utility for all actions
            action_values = np.full((3, ), -1000)
            # Explore all possible actions
            for action in action_list:
                action_values[action] = self.chance_node(agent=agent,
                                                         board_state=board_state.copy(),
                                                         action=action,
                                                         depth=depth)
            return np.max(action_values)

    def take_action(self, board_state, roll):
        actions = possible_actions(agent=self.eval_agent, board_state=board_state)

        # Create List of the Valid Actions
        action_list = list()
        for i, a in np.ndenumerate(actions):
            if a == 1:
                action_list.append(i)
        # Test Each Action and Determine it's Utility
        best_action = -1
        best_value = -1000
        for action in action_list:
            new_state = execute_action(agent=self.eval_agent, board_state=board_state.copy(), action=action, roll=roll)
            action_utility = self.expectiminimax(agent=self.eval_agent, board_state=new_state, depth=self.max_depth)
            if action_utility > best_value:
                best_value = action_utility
                best_action = action
        # Return the best action
        return best_action
