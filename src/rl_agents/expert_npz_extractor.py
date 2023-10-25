from gym_envs import FullAnchoringBaseline
from gym_envs import ExpertAnchorBaseline
from anch_human_demonstr import par1_cond1
from anch_human_demonstr import par1_cond2
from anch_human_demonstr import par1_cond3
from anch_human_demonstr import par1_cond1
from stable_baselines3.common.env_checker import check_env
import numpy as np

map_file = "../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_8.csv"

env = ExpertAnchorBaseline(map_file, par1_cond3)
#env = FullAnchoringBaseline(map_file)


actions = par1_cond3["actions"]
obs = env.reset()
obs = obs[0]

observation = []
actions_list = []
next_obs = []
dones = []
infos = []

for action in actions:
    # print(f"[{action},{obs}],")
    observation.append(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    actions_list.append(action)
    next_obs.append(obs)
    dones.append(terminated)
    infos.append(info)
    print(obs, reward, action)
    if terminated or truncated:
      print("AGENt REACHED GOAL")
      obs, info = env.reset()
      break


numpy_dict = {
            'obs': np.array(observation),
            'acts': np.array(actions_list),
            'next_obs': np.array(next_obs),
            'dones': np.array(dones),
            'infos': np.array(infos)
        }
for key, val in numpy_dict.items():
    print(key, val.shape)

save_path = "human_demonstr_data/human_dem_par1_cond3.npz"

if save_path is not None:
    np.savez(save_path, **numpy_dict)
