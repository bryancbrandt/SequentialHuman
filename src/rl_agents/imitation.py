import numpy as np
from stable_baselines3.common.monitor import Monitor
from updated_envs import FullAnchoringBaseline

from imitation.algorithms import bc
from imitation.data.types import Transitions

map_file = "../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_top_7.csv"
env = FullAnchoringBaseline(map_file)
env = Monitor(env)
expert_data = np.load("expert.npz", allow_pickle=True)
rng = np.random.default_rng(0)

transitions = Transitions(
    obs=expert_data['obs'],
    acts=expert_data['acts'],
    next_obs=expert_data['next_obs'],
    dones=expert_data['dones'],
    infos=expert_data['infos']
)

bc_trainer = bc.BC(
    observation_space=env.observation_space,
    action_space=env.action_space,
    demonstrations=transitions,
    rng=rng
)
bc_trainer.train(n_epochs=100)

obs = env.reset()
while True:
    action = bc_trainer.policy.predict(obs)[0]
    obs, reward, done, info = env.step(action)
    print(f"Obs:{obs}, R:{reward}, Done:{done}")
    if done:
        break
