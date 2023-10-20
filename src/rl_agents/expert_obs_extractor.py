from updated_envs import FullAnchoringBaseline
from updated_envs import ExpertAnchorBaseline
from anch_human_demonstr import par1_cond1
from stable_baselines3.common.env_checker import check_env
import numpy as np

map_file = "../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_1.csv"

# env = ExpertAnchorBaseline(map_file, par1_cond1)
env = FullAnchoringBaseline(map_file)

# actions = [3, 0, 3, 3, 0, 0, 3, 3, 0, 3, 0, 3, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 4,]
#actions = [3, 0, 3, 3, 0, 0, 3, 3, 0, 3, 0, 3, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 4, 3, 3, 0, 3, 3, 2, 3, 3, 3,
#           0, 0, 0, 1, 0, 1, 0, 0, 3, 3, 3, 4]

actions = [1,0,0,1,1,0,1,0,0,1,0,1,0,1,0,1,1,0,0,4, 0,1,0,0,3,0,3,0,3,0,3,0,3,0,3,3,3,2,3,4, 0,0,3,0,0,0,0,0,1,0,1,1,0,1,4, 1,1,1,1,1,4, 0,0,3,3,3,0,3,0,3,0,0,3,3,3,3,0,0,0,1,1,1,2,1,1,2,2,1,1,1,0,1,0,0,3,0,3,0,3,0,3,0]
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
