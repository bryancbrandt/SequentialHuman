from src.rl_agents.full_obs_anchoring import FullAnchoringBaseline

map_name = "../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_5.csv"
actions = [3, 0, 3, 0, 3, 0, 0, 0, 0, 0, 3, 3, 4, 1, 0, 1, 0, 1, 0, 1, 4, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 3, 3, 3, 0, 1, 0, 1, 0, 3, 1, 0, 0, 0, 1, 0, 1, 0, 1, 4, 0, 3, 4, 3, 0, 0, 3, 0, 3, 3, 0, 0, 0]
env = FullAnchoringBaseline(map_name)

for i in range(len(actions)):
    action = actions[i]
    action = int(action[0])
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"{action} {obs} {reward} {terminated}")
    if terminated or truncated:
      print("AGENt REACHED GOAL")
      obs, info = env.reset()
      break