import os
from abc import ABC

import gymnasium.utils.env_checker
import numpy as np
import gymnasium as gym
from gymnasium import spaces

from src.rl_agents.state_digraph import StateDiGraph

LAND = 0
HOUSE = 1
ROAD = 2
TREE = 3
START = 4
EXIT = 5
ROCK = 6
AMMO = 7
TANK = 9


def reward_normalize(distance: int, max_value: int):
    assert isinstance(distance, int), "Error distance must be an int"
    assert isinstance(max_value, int), "Error max_value must be an int"
    return 1 - (distance / max_value)


class AnchoringBaseline(gym.Env, ABC):
    metadata = {"render_modes": ["console"]}

    def __init__(self, map_csv: str, render_mode=None):
        assert isinstance(map_csv, str) and os.path.isfile(map_csv), "Error with map_csv argument!"
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # Load the map and set some local variables related to the map csv such as size, tank count, etc.
        self.map_csv = np.genfromtxt(map_csv, delimiter=",", dtype=int)
        row, col = self.map_csv.shape
        self._size = int(row * col)
        self._num_rows = row
        self._num_cols = col
        self._tank_count = int(np.count_nonzero(self.map_csv == TANK) / 2)
        self._agent_location = np.argwhere(self.map_csv == START)[0]  # row, col
        self._untraversable = [HOUSE, TREE, START, ROCK]
        self._tanks_destroyed = self._tank_count
        self._state_array = np.arange(0, row * col).reshape(row, col)  # State number table, used for returning obs
        self._agent_top = None  # Determines if the agent is working the top half or bottom half of map
        self._tank_list = []  # The current tank list that the agent can see
        self._reward_matrix = {}  # The reward matrix used for reward value lookup
        self._state_graph = StateDiGraph(map_csv, [LAND, ROAD, AMMO, TANK, START, EXIT])

        # We split the map into two different arrays: the top half and the bottom half
        mid_row = 10
        top_half = self.map_csv[:mid_row, :]
        bottom_half = self.map_csv[mid_row + 1:, :]

        # Now we get the tank locations for the top half and the bottom half, compensating for the bottom offset
        self._tank_loc_top = np.argwhere(top_half == TANK)
        self._tank_loc_bottom = np.argwhere(bottom_half == TANK)
        self._tank_loc_bottom = np.array([(lambda x: [x[0] + mid_row + 1, x[1]])(x) for x in self._tank_loc_bottom])

        # Get the exit locations for the top half and the bottom half
        self._exit_loc_top = np.argwhere(top_half == EXIT)
        self._exit_loc_bottom = np.argwhere(bottom_half == EXIT)
        self._exit_loc_bottom = np.array([(lambda x: [x[0] + mid_row + 1, x[1]])(x) for x in self._exit_loc_bottom])

        # Calculate the reward matrix.  The reward matrix is used instead of calculated reward values in real time.
        # Dictionary look up is much faster, however it can be a memory hog, but we are using servers with high RAM.
        # Reward values are calculated to each tank on the map, and each of the exits, even though only half of them
        # will be used.
        self._get_reward_matrix(top_half, self._exit_loc_top)
        self._get_reward_matrix(top_half, self._tank_loc_top)
        self._get_reward_matrix(bottom_half, self._exit_loc_bottom)
        self._get_reward_matrix(bottom_half, self._tank_loc_bottom)

        # Observations are dictionaries with the agent, tank, and exit locations.
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Discrete(self._size),
                "enemies": spaces.MultiDiscrete([self._size + 1 for _ in range(self._tank_count)], dtype=int),
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
            0: np.array([0, 1], dtype=int),  # Right
            1: np.array([-1, 0], dtype=int),  # Up
            2: np.array([0, -1], dtype=int),  # Left
            3: np.array([1, 0], dtype=int),  # Down
        }

    def _get_reward_matrix(self, array: np.ndarray, map_object: np.ndarray):
        """
        Adds a dictionary of reward values to the self._reward_matrix dictionary.  The key in the
        self._reward_matrix is a string: 'row,col' corresponding the location for each element
        of the map_object numpy 1-dimensional array.  The value for each key is a dictionary.
        This dictionary has keys corresponding to each cell from the numpy array parameter array.
        The values for each of these keys are determined by finding the normalized distance
        between the cell and the element of the map_object using dijkstra's shortest path, and
        subtracting this distance by 1.
        :param array: The numpy array associated with the current map, either top or bottom
        :param map_object: A list of targets for the player, usually the tanks or the exit for each top/bottom map
        :return: None
        """
        assert isinstance(array, np.ndarray), "Error! array must be a numpy array"
        assert isinstance(map_object, np.ndarray), "Error! map_object must be a numpy array"

        # Begin by iterating through each element of the map_object
        for element in map_object:
            # This is the dictionary that will be attached to each key in the self._reward_matrix
            # Each key corresponds to each element of the map_object.
            result_dict = {}
            location = ",".join([str(i) for i in element.tolist()])
            # Get the distance dictionary from the state digraph
            element_distance_dict = self._state_graph.distance_dict[location]
            # Find the cell with the greatest distance and get its value for distance normalization
            element_max_dist = max(element_distance_dict, key=lambda key: element_distance_dict[key])
            element_max_dist = element_distance_dict[element_max_dist]

            rows, cols = array.shape
            # Iterate through each cell of the passed array
            for i in range(rows):
                for j in range(cols):
                    # The try catch clause is used, because elements such as rocks are not in the digraph
                    # and will throw a KeyError
                    try:
                        # Get the current cell's distance to the current map object element
                        cell_key = f"{i},{j}"
                        cell_distance = element_distance_dict[cell_key]
                        # Calculate the reward value using the normalized distance function
                        reward_value = reward_normalize(cell_distance, element_max_dist)
                        result_dict[cell_key] = reward_value
                    except KeyError:
                        pass
            # Add the dictionary to the reward matrix using the element as the key name
            self._reward_matrix[location] = result_dict

    def _get_state(self, location: list) -> int:
        state = self._state_array[location[0]][location[1]]
        return int(state)

    def _get_obs(self):

        # Get the agent's state and the exit state
        agent_state = self._get_state(self._agent_location)
        exit_state = self._get_state(self._exit_location)

        # tank_location_states = list(map(self._get_state, self._tank_locations))
        tank_state = [self._size for _ in range(self._tank_count)]

        return {"agent": agent_state, "enemies": np.array(tank_state), "exit": exit_state}

    def _get_info(self):
        """
        Returns any needed additional information being passed from the environment
        :return: A dictionary containing key value pairs
        """
        return {}

    def _get_reward(self) -> float:
        """
        Calculates the reward granted after every state transition.  The reward structure
        works as follows:
        If the agent discovers 1 tank, the reward is the normalized linear Dijkstra's distance
        to that tank.  Meaning as the agent moves farther away, the rewards become more sparse.
        Alternatively, as the agent moves closer, the rewards increase in value.
        If the agent has discovered multiple tanks, the reward is the normalized linear Dijkstra's
        distance to the closest tank, if two tanks are the same distance, then one is chosen randomly.
        :return: Float value indicating reward
        """
        # If the agent is still at the starting position
        if self._agent_top is None:
            return 0.0

        # If the agent is navigating the top use the top tank locations
        elif self._agent_top:
            return 0.0

        # The agent is navigating the bottom map
        elif not self._agent_top:
            return 0.0

        # Otherwise...
        else:
            return 0.0

    def reset(self, seed=None, options=None):
        """
        Resets the game environment by initializing the player to their starting location,
        and seeding the random number generated (if needed)
        :param seed: the seed number for numpy random number generator
        :param options: Options passed to the gym environment
        :return:
        """
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Assign the agent's location
        self._agent_location = np.argwhere(self.map_csv == START)[0]
        self._tanks_destroyed = self._tank_count

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        """
        TODO: FILL THIS IN
        :param action:
        :return:
        """
        assert action in [0, 1, 2, 3, 4], "Error! Action must be 0, 1, 2, 3, 4"
        reward = 0
        terminated = False

        # If the action is a movement action
        if action in [0, 1, 2, 3]:
            direction = self._action_to_direction[action]
            new_state = self._agent_location + direction
            # Make sure we're still on the map
            if (0 <= new_state[0] < self._num_rows) and (0 <= new_state[1] < self._num_cols):
                # If the location being moved to is not in the untraversable list
                if self.map_csv[new_state[0]][new_state[1]] not in self._untraversable:
                    self._agent_location += direction

                    # If this is the first step toward top or bottom, set the agent top variable
                    if self._agent_top is None:
                        if action == 1:
                            self._agent_top = True
                        elif action == 3:
                            self._agent_top = False

                    # Don't allow an exit until all tanks have been destroyed
                    if self._tanks_destroyed <= 0:
                        # An episode is done iff the agent has reached the target
                        terminated = np.array_equal(self._agent_location, self._exit_location)

        # If the action is a weapons fire
        elif action == 4:
            # Determine if there is a tank close by using a distance metric?
            # self._shoot_tank()
            self._tanks_destroyed += 1

        reward = self._get_reward()
        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info

    def render(self):
        """
        This function is used for rendering, and is currently not implemented
        :return: None
        """
        if self.render_mode == "console":
            pass


env = AnchoringBaseline("../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_1.csv")
