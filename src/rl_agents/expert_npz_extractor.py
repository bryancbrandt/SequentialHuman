from updated_envs import FullAnchoringBaseline
from updated_envs import ExpertAnchorBaseline
from anch_human_demonstr import participant1_condition1
from stable_baselines3.common.env_checker import check_env
import numpy as np

map_file = "../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_top_7.csv"

# env = ExpertAnchorBaseline(map_file, participant1_condition1)
env = FullAnchoringBaseline(map_file)


actions = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 3, 3, 0, 1, 0, 1, 0, 3, 3, 0, 3, 0, 1, 1, 2, 1, 1, 1, 4, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 4, 1, 1, 2, 1, 1, 0, 0, 1, 0, 0, 3, 3, 0, 3, 3, 3, 2, 3, 2, 2, 3, 2, 3, 3, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 3, 0, 1, 0, 1, 0, 0, 4, 1, 1, 4, 0, 3, 3, 3, 3, 3, 3, 3, 3, 4, 2, 2, 1, 2, 1, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 1, 1, 0, 1, 2, 1, 2, 1, 2, 1, 0, 1, 2, 2, 2, 2, 1, 0, 1, 0, 1, 0, 0, 0, 0, 3, 0, 3, 1, 0, 0, 0, 0, 3, 2, 2, 3, 2, 3, 3, 0, 3, 3, 3, 2, 3, 2, 0, 0, 1, 0, 1, 0, 1, 1]

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

save_path = "expert.npz"

if save_path is not None:
    np.savez(save_path, **numpy_dict)
