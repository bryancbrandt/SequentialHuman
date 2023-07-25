import os
from abc import ABC
import numpy as np
import gymnasium as gym
from gymnasium import spaces

HOUSE = 1
ROAD = 2
TREE = 3
START = 4
EXIT = 5
ROCK = 6
AMMO = 7
TANK = 9


class AnchoringBaseline(gym.Env, ABC):
    metadata = {"render_modes": ["console"]}

    def __init__(self, map_csv: str, render_mode=None):
        assert isinstance(map_csv, str) and os.path.isfile(map_csv), "Error with map_csv argument!"
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # Load the map and set some local variables related to the csv such as size, tank count, etc.
        self.map_csv = np.genfromtxt(map_csv, delimiter=",", dtype=int)
        row, col = self.map_csv.shape
        self._size = row * col
        self._num_rows = row
        self._num_cols = col
        self._tank_count = int(np.count_nonzero(self.map_csv == TANK) / 2)
        self._agent_location = np.argwhere(self.map_csv == START)[0]  # row, col
        self._tank_locations = np.argwhere(self.map_csv == TANK)  # row, col
        self._exit_location = np.argwhere(self.map_csv == EXIT)[0]
        self._un_traversable = [HOUSE, TREE, START, ROCK]
        self._tanks_destroyed = 0
        self._state_array = np.arange(0, row * col).reshape(row, col)

        # Observations are dictionaries with the agent's and the target's location.
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Discrete(self._size),
                "enemies": spaces.MultiDiscrete([self._size for _ in range(self._tank_count)]),
                "exit": spaces.Discrete(self._size)
            }
        )

        # There are 4 actions corresponding to "right", "up", "left", "down", "fire"
        self.action_space = spaces.Discrete(5)

        """
        The following dictionary maps abstract actions from `self.action_space` to
        the direction we will walk in if that action is taken. [row, col]
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([0, 1]),  # Right
            1: np.array([-1, 0]),  # Up
            2: np.array([0, -1]),  # Left
            3: np.array([1, 0]),  # Down
        }

    def _get_state(self, location: list) -> int:
        state = self._state_array[location[0]][location[1]]
        return state

    def _get_obs(self):
        agent_state = self._get_state(self._agent_location)
        # tank_state = list(map(self._get_state, self._tank_locations))
        tank_state = [-1 for _ in range(self._tank_count)]
        exit_state = self._get_state(self._exit_location)
        return {"agent": agent_state, "enemies": tank_state, "exit": exit_state}

    def _get_info(self):
        return {}

    def reset(self, seed=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Assign the agent's location
        self._agent_location = np.argwhere(self.map_csv == START)[0]
        self._tank_locations = np.argwhere(self.map_csv == TANK)
        self._exit_location = np.argwhere(self.map_csv == EXIT)[0]
        self._tanks_destroyed = 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        reward = 0
        terminated = False
        # If the action is a movement action
        if action in [0, 1, 2, 3]:
            direction = self._action_to_direction[action]
            new_state = self._agent_location + direction
            # If the location being moved to is not in the untraversable list
            if self.map_csv[new_state[0]][new_state[1]] not in self._un_traversable:
                # Make sure we're still on the map
                if (0 <= direction[0] < self._num_rows) and (0 <= direction[1] < self._num_cols):
                    self._agent_location += direction
                    reward = 1
                    # Don't allow an exit until all tanks have been destroyed
                    if self._tanks_destroyed <= 0:
                        # An episode is done iff the agent has reached the target
                        terminated = np.array_equal(self._agent_location, self._exit_location)
                        # TODO: FIX THIS PROBLEM WITH THE REWARD VALUES
                        reward = 1000

        # If the action is a weapons fire
        elif action == 4:
            # Determine if there is a tank close by using a distance metric?
            self._tanks_destroyed += 1
            reward = 100

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, info

    def render(self):
        if self.render_mode == "console":
            pass


bsl = AnchoringBaseline("../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_1.csv")
print(bsl.step(1))