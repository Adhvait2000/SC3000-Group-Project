# SC3000-Artifical Intelligence 

# Introduction

The cartpole problem is a classic reinforcement learning problem that involves balancing a pole on a cart that moves along a horizontal track. The objective is to keep the pole balanced for as long as possible by controlling the movement of the cart. 

# Dependencies 

To solve the cartpole problem using Q-learning and the gym environment, we used the following dependencies:
1. Python3
2. NumPy
3. gym

# Tasks

1. Development of an RL agent

We utilized Q-learning to develop the agent. 

Reason for choosing Q-learning:
  - Q-learning is one of the most popular and effective reinforcement learning algorithm
  - Q-learning is a model-free algorithm, meaning it does not require knowledge of the underlying dynamics of the system being controlled.
  - Q-learning is a value-based method, meaning it learns a value function that maps states to action values. In the cartpole problem, the agent needs to learn which actions are best to take in different states, and  a value-based approach like Q-learning can effectively learn the optimal action values for each state.

2. Demonstrate the effectiveness of the RL agent

After training the agent using Q-learning, we ran the agent over 100 episodes and plotted a cumulative reward against all episodes in Jupyter. The average reward we achieved was 275.

3. Render 1 episode played by the developed RL agent on Jupyter

Using the trained agent, we rendered the cartpole balancing problem through PyGame. 
