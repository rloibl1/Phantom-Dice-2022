# Script file to benchmark various AI Algorithms
from random_action import RandomAgent
from greedy_action import GreedyAgent
from monte_carlo_rollout import MonteCarloAgent
from expectiminimax import MinimaxAgent
from AI_library import benchmark

# Random vs Random
agent_a = RandomAgent(agent=0)
agent_b = RandomAgent(agent=1)
wins, losses, ties = benchmark(agent_a=agent_a, agent_b=agent_b, matches=1000)
print(f"Agent A (Random) performance: {wins}/{losses}/{ties}")

# Greedy vs Random
agent_a = GreedyAgent(agent=0)
agent_b = RandomAgent(agent=1)
wins, losses, ties = benchmark(agent_a=agent_a, agent_b=agent_b, matches=1000)
print(f"Agent A (Greedy) performance: {wins}/{losses}/{ties}")

# Monte-Carlo-10 vs Random
agent_a = MonteCarloAgent(agent=0, trials=10)
agent_b = RandomAgent(agent=1)
wins, losses, ties = benchmark(agent_a=agent_a, agent_b=agent_b, matches=100)
print(f"Agent A (Monte-Carlo-10) performance: {wins}/{losses}/{ties}")

# Monte-Carlo-50 vs Random
# agent_a = MonteCarloAgent(agent=0, trials=50)
# agent_b = RandomAgent(agent=1)
# wins, losses, ties = benchmark(agent_a=agent_a, agent_b=agent_b, matches=100)
# print(f"Agent A (Monte-Carlo-50) performance: {wins}/{losses}/{ties}")

# Monte-Carlo-250 vs Random
# agent_a = MonteCarloAgent(agent=0, trials=250)
# agent_b = RandomAgent(agent=1)
# wins, losses, ties = benchmark(agent_a=agent_a, agent_b=agent_b, matches=100)
# print(f"Agent A (Monte-Carlo-250) performance: {wins}/{losses}/{ties}")

# Minimax-3 vs Random
agent_a = MinimaxAgent(eval_agent=1, max_depth=0)
agent_b = RandomAgent(agent=1)
wins, losses, ties = benchmark(agent_a=agent_a, agent_b=agent_b, matches=100)
print(f"Agent A (Minimax-3) performance: {wins}/{losses}/{ties}")
