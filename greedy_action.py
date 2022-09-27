# Agent that takes the best possible current move every turn

import random
import time
from AI_library import *


class GreedyAgent:
    def __init__(self, agent):
        self.agent = agent

    def take_action(self, board_state, roll):
        actions = possible_actions(agent=self.agent, board_state=board_state)

        # Create List of the Valid Actions
        action_list = list()
        for i, a in np.ndenumerate(actions):
            if a == 1:
                action_list.append(i)

        # Test Each Action and Determine it's Utility
        best_action = -1
        best_value = -1000
        for action in action_list:
            new_state = execute_action(agent=self.agent, board_state=board_state.copy(), action=action, roll=roll)
            action_utility = calculate_utility(agent=self.agent, board_state=new_state)
            if action_utility > best_value:
                best_value = action_utility
                best_action = action
        # Return the best action
        return best_action
