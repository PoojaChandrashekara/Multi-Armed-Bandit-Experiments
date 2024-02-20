# -*- coding: utf-8 -*-
"""Project1_PC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17ea-VTfGHZJqTurDRll846ylbb2GVgDi
"""





import numpy as np
import matplotlib.pyplot as plt

# Define reward functions for each arm
def arm1():
    return np.random.normal(5, 10)

def arm2():
    if np.random.rand() < 0.5:
        return np.random.normal(10, 15)
    else:
        return np.random.normal(4, 10)

# Define functions for each alpha value
def alpha1(k):
    return 1

def alpha2(k):
    return 0.9 ** k

def alpha3(k):
    return 1 / (1 + np.log(1 + k))


def alpha4(k):
    return 1 / k

# Initialize Q-values to zero
Q = np.zeros((2, 100))

# Define hyperparameters
epsilons = [0, 0.1, 0.2, 0.5]
alpha_funcs = [alpha1, alpha2, alpha3, alpha4]

# Run simulations
rewards = np.zeros((len(epsilons), len(alpha_funcs), 1000))
avg_q_values = np.zeros((len(epsilons), len(alpha_funcs), 2))
for i, epsilon in enumerate(epsilons):
    for j, alpha_func in enumerate(alpha_funcs):
        avg_qs = np.zeros((100, 2))
        for k in range(100):
            # Reset Q-values at the beginning of each run
            Q = np.zeros((2, 100))
            for t in range(1, 1001):
                # Select action according to epsilon-greedy policy
                if np.random.rand() < epsilon:
                    action = np.random.randint(2)
                else:
                    action = np.argmax(Q[:, 0])
                # Observe reward and update Q-values
                if action == 0:
                    reward = arm1()
                else:
                    reward = arm2()
                alpha = alpha_func(t)
                Q[action, k] += alpha * (reward - Q[action, k])
                # Compute average accumulated reward
                rewards[i, j, t-1] += Q.sum() / (100 * t)
            # Compute average Q-values for current run
            avg_q1 = np.mean(Q[0, -1])
            avg_q2 = np.mean(Q[1, -1])
            # Store average Q-values for current run
            avg_qs[k] = (avg_q1, avg_q2)
        # Compute average Q-values over 100 runs
        avg_q1, avg_q2 = np.mean(avg_qs, axis=0)
        avg_q_values[i, j, 0] = avg_q1
        avg_q_values[i, j, 1] = avg_q2

# Plot results
for j, alpha_func in enumerate(alpha_funcs):
    plt.figure()
    for i, epsilon in enumerate(epsilons):
        plt.plot(rewards[i, j, :], label=f"epsilon={epsilon}")
        avg_q1 = avg_q_values[i, j, 0]
        avg_q2 = avg_q_values[i, j, 1]
        print(f"Epsilon: {epsilon}, Alpha: {alpha_func.__name__}, Q(a1): {avg_q1:.2f}, Q(a2): {avg_q2:.2f}")
    plt.legend()
    plt

import numpy as np
import matplotlib.pyplot as plt

# Define the environment
num_actions = 2
num_steps = 1000
true_rewards = np.random.randn(num_actions)

# Define the initial Q-values
initial_Qs = [[0, 0], [5, 7], [20, 20]]

# Define the learning rate and epsilon
alpha = 0.1
EPSILON = 0.1

# Define the number of runs
num_runs = 100

# Initialize arrays to store the results
accumulated_rewards = np.zeros((num_runs, num_steps, len(initial_Qs)))
avg_qs = np.zeros((len(initial_Qs), num_actions))

# Loop over the initial Q-values
for k, initial_Q in enumerate(initial_Qs):
    # Loop over the runs
    for i in range(num_runs):
        # Initialize the Q-values and rewards
        Q = np.array([initial_Q] * num_steps)
        rewards = np.zeros(num_steps)

        # Loop over the steps
        for t in range(num_steps):
            # Choose an action using epsilon-greedy policy
            if np.random.rand() < EPSILON:
                action = np.random.randint(num_actions)
            else:
                action = np.argmax(Q[t])

            # Observe the reward for the chosen action
            reward = true_rewards[action] + np.random.randn()

            # Update the Q-value for the chosen action using the learning rate
            Q[t][action] += alpha * (reward - Q[t][action])

            # Store the reward
            rewards[t] = reward

        # Compute the accumulated reward for the run
        accumulated_reward = np.cumsum(rewards)
        accumulated_rewards[i, :, k] = accumulated_reward

        # Compute average Q-values for current run
        avg_q1 = np.mean(Q[:, 0])
        avg_q2 = np.mean(Q[:, 1])
        # Store average Q-values for current run
        avg_qs[k] += np.array([avg_q1, avg_q2])

    # Compute average Q-values over 100 runs
    avg_qs[k] /= num_runs

# Plot the results
for k, initial_Q in enumerate(initial_Qs):
    plt.plot(np.mean(accumulated_rewards[:, :, k], axis=0), label=f'[{initial_Q[0]}, {initial_Q[1]}]')
plt.xlabel('Steps')
plt.ylabel('Accumulated Reward')
plt.legend()
plt.show()

# Print the average Q-values
for k, initial_Q in enumerate(initial_Qs):
    print(f"Average Q-values for initial Q-values [{initial_Q[0]}, {initial_Q[1]}]: Q(a1) = {avg_qs[k][0]:.2f}, Q(a2) = {avg_qs[k][1]:.2f}")

import numpy as np
import matplotlib.pyplot as plt

# Define the number of arms and the number of steps
n_arms = 2
n_steps = 1000

# Define the true reward probabilities for each arm
true_probs = np.array([0.3, 0.5])

# Initialize the action values and preference values for each arm
action_values = np.zeros(n_arms)
preferences = np.zeros(n_arms)

# Initialize the array to store the accumulated reward at each time step
reward_history = np.zeros(n_steps)

# Define the softmax function to compute the action probabilities
def softmax(preferences):
    exp_preferences = np.exp(preferences)
    return exp_preferences / np.sum(exp_preferences)

# Run the Gradient-Bandit algorithm for n_steps
for t in range(n_steps):
    # Compute the action probabilities using the softmax function
    action_probs = softmax(preferences)

    # Choose an action using the action probabilities
    chosen_action = np.random.choice(np.arange(n_arms), p=action_probs)

    # Generate a reward for the chosen action
    reward = np.random.binomial(1, true_probs[chosen_action])

    # Update the reward history
    reward_history[t] = reward

    # Update the average reward
    avg_reward = np.mean(reward_history[:t+1])

    # Update the preferences and action values
    for a in range(n_arms):
        if a == chosen_action:
            preferences[a] += 0.1 * (reward - avg_reward) * (1 - action_probs[a])
        else:
            preferences[a] -= 0.1 * (reward - avg_reward) * action_probs[a]

    # Print the current step and average reward
    print(f"Step {t+1}, Average reward: {avg_reward:.2f}")

# Plot the average accumulated reward with respect to step/time
plt.plot(np.arange(n_steps), np.cumsum(reward_history) / np.arange(1, n_steps+1))
plt.xlabel("Time step")
plt.ylabel("Average accumulated reward")
plt.title("Gradient-Bandit algorithm with alpha=0.1")
plt.show()