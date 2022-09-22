# Algorithm that takes a random action
import numpy as np
import random
import time
from AI_library import *


class RandomAgent:
    def __init__(self, agent):
        self.agent = agent

    def take_action(self, board_state, roll):
        actions = possible_actions(agent=self.agent, board_state=board_state)

        # Create List of the Valid Actions
        action_list = list()
        for i, a in np.ndenumerate(actions):
            if a == 1:
                action_list.append(i[0])

        # Return a Random Valid Action
        return random.choice(action_list)
