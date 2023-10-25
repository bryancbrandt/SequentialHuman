import numpy as np
from stable_baselines3 import DQN
from nltk.translate import meteor_score
from stable_baselines3.common.monitor import Monitor
from gym_envs import ExpertAnchorBaseline
from anch_human_demonstr import par1_cond1
import nltk


expert_data = np.load("./human_demonstr_data/human_dem_par1_cond1.npz", allow_pickle=True)

map = "../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_top_10.csv"
condition = par1_cond1
env = ExpertAnchorBaseline(map, condition)
env = Monitor(env)

model = DQN("MlpPolicy", env, verbose=1)
file = "reward_shaped_agents/DQN_RS_participant1_condition1.zip"
model = model.load("DQN_RS_participant1_condition1.zip")


# Build a list of the 'wordings' from the set of expert trajectories
# a wording consists of "obs, action".  These are added as strings
# since the METEOR method requires strings.  Since we are iterating through
# all observations too, we can simultaneously build the expert
# trajectory object to be passed to dagger.
expert_trajectory_list = []
expert_trajectory = []
trajectory_list = []

for i in range(len(expert_data["obs"])):
    # Build the word for the Meteor score and add it to the
    # expert trajectory list
    word = str(expert_data["obs"][i]) + "," + str(expert_data["acts"][i])
    expert_trajectory.append(word)

agent_trajectory = []
for i in range(1000):
    obs = env.reset()
    obs = obs[0]
    total_reward = 0
    while True:
        action = model.predict(obs)
        action = int(action[0])
        word = str(obs) + "," + str(action)
        agent_trajectory.append(word)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

        if terminated:
            print(f"{total_reward}", end="")
            for trajs in expert_trajectory_list:
                score = meteor_score.single_meteor_score(trajs, agent_trajectory)
                print(f", {score}", end="")
            print()
            agent_trajectory = []
            break
