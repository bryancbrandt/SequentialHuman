from gym_envs import FullAnchoringBaseline
from gym_envs import ExpertAnchorBaseline
from anch_human_demonstr import par1_cond1
from anch_human_demonstr import par1_cond2
from anch_human_demonstr import par1_cond3
from stable_baselines3.common.env_checker import check_env
import numpy as np

map_file = "../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_8.csv"

env = ExpertAnchorBaseline(map_file, par1_cond3)
#env = FullAnchoringBaseline(map_file)

actions = par1_cond3["actions"]
obs = env.reset()
obs = obs[0]
obs_list = []

for action in actions:
    obs_list.append([list(obs), action])
    obs, reward, terminated, truncated, info = env.step(action)
    print(obs_list[-1], reward)
    if terminated or truncated:
        print("AGENt REACHED GOAL")
        obs, info = env.reset()
        break


print("*****************************************")
print(obs_list)
