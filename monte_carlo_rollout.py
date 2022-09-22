# Monte Carlo Simulation Algorithm - samples x number of random games for each possible next move

import time
from AI_library import *


class MonteCarloAgent:
    def __init__(self, agent, trials):
        self.agent = agent
        self.trials = trials

    def take_action(self, board_state, roll):
        actions = possible_actions(agent=self.agent, board_state=board_state)
        # print(actions)

        # Create List of the Valid Actions
        action_list = list()
        for i, a in np.ndenumerate(actions):
            if a == 1:
                action_list.append(i[0])

        # Test Each Action and Determine it's Utility
        best_action = None
        best_value = -1000
        win_chance = None
        for action in action_list:
            new_state = execute_action(agent=self.agent, board_state=board_state.copy(), action=action, roll=roll)
            cum_value = 0
            wins = 0
            for trial in range(self.trials):
                outcome, value = execute_game(agent=self.agent, board_state=new_state)
                wins += outcome
                cum_value += value
            avg_value = cum_value / self.trials
            # Check if this action is better
            if avg_value > best_value:
                best_action = action
                best_value = avg_value
                win_chance = round(wins / self.trials, 4)
        # Return the best action
        # print(f"Best Action: {best_action} with average value of {best_value} win rate {win_chance}")
        return best_action
