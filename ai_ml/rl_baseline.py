# rl_baseline.py
# A baseline Reinforcement Learning model (Multi-Armed Bandit)
# for the SmartSeat project (CP3405).
# [cite_start]Objective: "Optimize real-time seat allocation policies" 

import numpy as np
import random

class SeatAllocationBandit:
    """
    Implements a Multi-Armed Bandit (MAB) simulation using Epsilon-Greedy.
    Each "arm" represents a different seat allocation strategy.
    """
    
    def __init__(self, k_arms, epsilon=0.1):
        """
        Initialize the bandit.
        :param k_arms: The number of allocation strategies (arms).
        :param epsilon: The probability of exploring (choosing a random arm).
        """
        self.k_arms = k_arms
        self.epsilon = epsilon
        
        # q_values: The estimated average reward for each arm (strategy)
        self.q_values = np.zeros(k_arms)
        # n_pulls: The number of times each arm has been pulled (tried)
        self.n_pulls = np.zeros(k_arms)
        
        print(f"Initialized Multi-Armed Bandit with {k_arms} arms and epsilon={epsilon}")

    def choose_strategy(self):
        """
        Choose a strategy (arm) using the Epsilon-Greedy policy.
        """
        if random.random() < self.epsilon:
            # --- EXPLORE ---
            # Choose a random arm (strategy)
            return np.random.randint(self.k_arms)
        else:
            # --- EXPLOIT ---
            # Choose the arm with the highest current Q-value (best-known strategy)
            return np.argmax(self.q_values)

    def update_policy(self, arm_index, reward):
        """
        Update the Q-value for the chosen arm based on the reward received.
        """
        # Increment the pull count for this arm
        self.n_pulls[arm_index] += 1
        
        # Update the average reward (Q-value) using incremental mean
        # Q_new = Q_old + (1/N) * (Reward - Q_old)
        n = self.n_pulls[arm_index]
        old_q = self.q_values[arm_index]
        new_q = old_q + (1/n) * (reward - old_q)
        
        self.q_values[arm_index] = new_q

# --- Simulation ---

def run_simulation():
    """
    Runs a simulation to test the MAB model.
    """
    print("\n--- Starting RL Simulation for Seat Allocation ---")
    
    # Define our "arms" (strategies) and their "true" success probabilities.
    # The agent does NOT know these probabilities; it must learn them.
    [cite_start]# [cite: 80] Arm 0: "Assign Accessible Seat" (for Priya) - High success, but for specific users
    [cite_start]# [cite: 79] Arm 1: "Assign Near Door" (for Alex) - Medium success, fast
    # Arm 2: "Assign Quiet Zone" - High success for most students
    # Arm 3: "Assign Randomly" - Low success (baseline)
    
    # Let's simplify and assume these are the general success rates for all students
    strategy_names = [
        "Strategy 1: Assign Accessible Zone",
        "Strategy 2: Assign Near Door",
        "Strategy 3: Assign Quiet Zone",
        "Strategy 4: Assign Randomly"
    ]
    true_probabilities = np.array([0.7, 0.5, 0.9, 0.3])
    k = len(strategy_names)

    print(f"The 'ground truth' success rates (unknown to the agent) are: {true_probabilities}")
    
    # Initialize our agent
    agent = SeatAllocationBandit(k_arms=k, epsilon=0.1)
    
    # Define the simulation parameters
    n_simulations = 1000
    
    # Run the simulation
    for i in range(n_simulations):
        # 1. Agent chooses a strategy (arm)
        chosen_arm = agent.choose_strategy()
        
        # 2. Environment gives a reward
        # Simulate success/failure based on the true probability
        if random.random() < true_probabilities[chosen_arm]:
            reward = 1  # Success
        else:
            reward = 0  # Failure
            
        # 3. Agent updates its policy
        agent.update_policy(chosen_arm, reward)

    # --- Results ---
    print("\n--- Simulation Complete ---")
    print(f"Ran {n_simulations} simulations.")
    
    print("\nFinal Learned Q-Values (Agent's belief of success rate):")
    for i in range(k):
        print(f"  {strategy_names[i]:<30}: {agent.q_values[i]:.4f} (Tried {agent.n_pulls[i]} times)")

    print("\nComparison to Ground Truth:")
    print(f"  True Probabilities: {true_probabilities}")
    print(f"  Learned Values:     {np.round(agent.q_values, 2)}")
    
    best_strategy_index = np.argmax(agent.q_values)
    print(f"\nConclusion: The agent learned that '{strategy_names[best_strategy_index]}' is the optimal policy.")

# Main entry point to run the script
if __name__ == "__main__":
    run_simulation()