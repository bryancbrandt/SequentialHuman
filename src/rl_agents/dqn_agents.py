import gymnasium as gym

from stable_baselines3 import DQN

from src.rl_agents.gym_envs import AnchoringBaseline

env = AnchoringBaseline("../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_1.csv")

model = DQN("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000, log_interval=4)

obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()