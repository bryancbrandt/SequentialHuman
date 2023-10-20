import gymnasium as gym
import numpy as np
import os
from abc import ABC
from gymnasium import spaces
from src.rl_agents.state_digraph import StateDiGraph
from scipy.spatial.distance import cityblock
import networkx as nx

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


def get_subarray(large_array, row_idx, col_idx, subarray_size=20):
    array_shape = large_array.shape
    subarray_radius = subarray_size // 2

    # Calculate the range of rows and columns to extract
    row_start = max(row_idx - subarray_radius, 0)
    row_end = min(row_idx + subarray_radius + 1, array_shape[0])
    col_start = max(col_idx - subarray_radius, 0)
    col_end = min(col_idx + subarray_radius + 1, array_shape[1])

    # Extract the subarray
    subarray = large_array[row_start:row_end, col_start:col_end]

    return subarray, (row_start, col_start)


def get_state_string(first, second):
    return f"{first},{second}"


class FullAnchoringBaseline(gym.Env, ABC):
    metadata = {"render_modes": ["console"]}

    def __init__(self, map_csv: str, render_mode=None):
        assert isinstance(map_csv, str) and os.path.isfile(map_csv), "Error with map_csv argument!"
        assert render_mode is None or render_mode in self.metadata["render_modes"]

        self.render_mode = render_mode
        self._map_name = map_csv

        # Load the map and set some local variables related to the map csv such as size, tank count, etc.
        self.map_csv = np.genfromtxt(map_csv, delimiter=",")
        row, col = self.map_csv.shape
        self._size = int(row * col)
        self._num_rows = row
        self._num_cols = col
        self._tank_count = int(np.count_nonzero(self.map_csv == TANK) / 2)  # How many tanks for each half of the map
        self._agent_location = np.argwhere(self.map_csv == START)[0]  # row, col
        self._untraversable = [HOUSE, TREE, START, ROCK]  # What the agent cannot traverse
        self._state_array = np.arange(0, row * col).reshape(row, col)  # State number table, used for returning obs
        self._agent_top = None  # Determines if the agent is working the top half or bottom half of map
        self._tank_list = []  # The tanks from the map
        self._tanks_destroyed = []  # The list of tanks that have been destroyed
        self._reward_matrix = {}  # The reward matrix used for reward value lookup
        self._state_graph = StateDiGraph(map_csv, [LAND, ROAD, AMMO, TANK, START, EXIT])  # Digraph of the env
        self._target = None  # The current target of the enemy.  Either a tank, or the exit
        self.episode_length = 0  # Initialize episode length

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
        self._get_reward_matrix(bottom_half, self._exit_loc_bottom, True)
        self._get_reward_matrix(bottom_half, self._tank_loc_bottom, True)

        # Observations are dictionaries with the agent, tank, and exit locations.
        # We use self._size + 1, so that the highest value signifies a null value since spaces does not allow null

        self.observation_space = spaces.MultiDiscrete([self._size, self._size + 1, self._size + 1])
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

    def _check_radar(self) -> bool:

        subarray_size = 2

        if self._agent_top is None:
            vision_array = np.array([])
        elif self._agent_top:
            vision_array, (start_row, start_col) = get_subarray(self.map_csv[:10, :], self._agent_location[0],
                                                                self._agent_location[1], subarray_size=subarray_size)
        elif not self._agent_top:
            vision_array, (start_row, start_col) = get_subarray(self.map_csv[11:, :], self._agent_location[0] - 11,
                                                                self._agent_location[1], subarray_size=subarray_size)
            start_row += 11
        else:
            vision_array = np.array([])

        tank_locations = np.argwhere(vision_array == TANK)

        # If the tank is within the 3 x 3 vision field, destroy the first tank
        # and set its value on the map csv to 0 to prevent re-targeting
        if len(tank_locations) > 0:
            tank = tank_locations[0]
            row_in_subarray, col_in_subarray = tank[0], tank[1]

            row_tank_map_loc = start_row + row_in_subarray
            col_tank_map_loc = start_col + col_in_subarray

            location = [row_tank_map_loc, col_tank_map_loc]
            if location not in self._tanks_destroyed:
                self._tanks_destroyed.append(location)
                self.map_csv[row_tank_map_loc][col_tank_map_loc] = 0
                return True
        else:
            return False

    def _get_closest_objective(self):

        if len(self._tanks_destroyed) == self._tank_count:

            if self._agent_top:
                self._target = self._exit_loc_top[0]
            elif not self._agent_top:
                self._target = self._exit_loc_bottom[0]
            else:
                self._target = None

        # Anything else, the target should be the closest tank
        else:

            # Make sure the tank list is occupied
            if self._tank_list is not None:

                min_distance = float('inf')
                current_location = get_state_string(self._agent_location[0], self._agent_location[1])

                for tank in self._tank_list:

                    if tank not in self._tanks_destroyed:

                        tank_name = get_state_string(tank[0], tank[1])
                        # Calculate primary distance using dijkstra
                        distance = self._state_graph.distance_dict[current_location][tank_name]
                        # Calculate secondary distance using manhattan
                        manhattan_distance = cityblock(self._agent_location, tank)
                        # Combine primary and secondary distance measures
                        combined_distance = 0.7 * distance + 0.3 * manhattan_distance
                        if combined_distance < min_distance:
                            min_distance = combined_distance
                            self._target = tank
            else:
                Exception("Error! Tank list is empty in get closest objective method")

    def _get_info(self) -> dict:
        """
        Returns any needed additional information being passed from the environment
        :return: A dictionary containing key value pairs
        """
        return {}

    def _get_obs(self) -> dict:
        """
        Returns the observation information of the environment.  Converts the cell location to a state number for
        the agent, the tank locations, and the exit locations.  Returns these values as a dictionary.
        :return:
        """
        # Get the agent's state and the exit state
        agent_state = self._get_state(self._agent_location)
        if self._agent_top is None:
            exit_state = self._size  # Null value
            tank_states = [self._size for _ in range(self._tank_count)]
        elif self._agent_top:
            exit_state = self._get_state(self._exit_loc_top[0])
            tank_states = []
            for tank in self._tank_list:
                tank_states.append(self._get_state(tank))
        elif not self._agent_top:
            exit_state = self._get_state(self._exit_loc_bottom[0])
            tank_states = []
            for tank in self._tank_list:
                tank_states.append(self._get_state(tank))
        else:
            exit_state = self._size  # Null value
            tank_states = [self._size for _ in range(self._tank_count)]

        # Get the current target
        if self._target is None:
            target_state = 840
        else:
            target_state = self._get_state(self._target)

        return np.array([agent_state, target_state, exit_state])

    def _get_reward(self) -> float:
        """
        Return the reward based upon the agent's location and discoveries.  If no tanks have been discovered
        then the returned reward is 0.0.  If there is at least 1 tank that is discovered, the highest reward
        is returned based upon the self._reward_matrix
        :return: Float value indicating reward
        """
        # If the agent is still at the starting position
        if self._agent_top is None:
            return 0.0

        # If the agent is navigating the top, get the reward
        elif self._agent_top:

            # If all the tanks are destroyed, the reward is calculated to the exit
            agent_location = get_state_string(self._agent_location[0], self._agent_location[1])
            if len(self._tanks_destroyed) == self._tank_count:
                if np.array_equal(self._agent_location, self._exit_loc_top[0]):
                    return 1000
                else:
                    exit_location = get_state_string(self._exit_loc_top[0][0], self._exit_loc_top[0][1])
                    return self._reward_matrix[exit_location][agent_location]
            # The reward is to the closest tank
            elif self._target is not None:
                tank_location = get_state_string(self._target[0], self._target[1])
                return self._reward_matrix[tank_location][agent_location]
            # Everything else is zero
            else:
                return 0.0

        # The agent is navigating the bottom get the reward
        elif not self._agent_top:

            agent_location = get_state_string(self._agent_location[0], self._agent_location[1])
            if len(self._tanks_destroyed) == self._tank_count:
                if np.array_equal(self._agent_location, self._exit_loc_bottom[0]):
                    return 1000
                else:
                    exit_location = get_state_string(self._exit_loc_bottom[0][0], self._exit_loc_bottom[0][1])
                    return self._reward_matrix[exit_location][agent_location]
            elif self._target is not None:
                tank_location = get_state_string(self._target[0], self._target[1])
                return self._reward_matrix[tank_location][agent_location]
            else:
                return 0.0

        # Otherwise...
        else:
            return 0.0

    def _get_reward_matrix(self, array: np.ndarray, map_object: np.ndarray, is_bottom: bool = False):
        """
        Adds a dictionary of reward values to the self._reward_matrix dictionary.  The key in the
        self._reward_matrix is a string: 'row,col' corresponding the location for each element
        of the map_object numpy 1-dimensional array.  The value for each key is a dictionary.
        This dictionary has keys corresponding to each cell from the numpy array parameter array.
        The values for each of these keys are determined by finding the normalized distance
        between the cell and the element of the map_object using dijkstra's shortest path, and
        subtracting this distance from 1 to get the reward value.
        :param array: The numpy array associated with the current map, either top or bottom
        :param map_object: A list of targets for the player, usually the tanks or the exit for each top/bottom map
        :return: None
        """
        assert isinstance(array, np.ndarray), "Error! array must be a numpy array"
        assert isinstance(map_object, np.ndarray), "Error! map_object must be a numpy array"

        # First we create a graph network for the passed map, and create a distance dictionary
        rows, cols = array.shape

        graph = nx.DiGraph()

        # Iterate through the array
        for i in range(rows):
            for j in range(cols):
                cell_value = self.map_csv[i, j]

                # Check if the cell value is in the allowed_values list
                if cell_value not in self._untraversable:
                    # Add the cell value as a node to the graph
                    if is_bottom:
                        node_name = get_state_string(i + 11, j)
                    else:
                        node_name = get_state_string(i, j)
                    graph.add_node(node_name, value=cell_value)

                    # Check and add directed edges to neighboring cells
                    neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                    for ni, nj in neighbors:
                        if 0 <= ni < rows and 0 <= nj < cols and array[ni, nj] not in self._untraversable:
                            if is_bottom:
                                neighbor_name = get_state_string(ni + 11, nj)
                            else:
                                neighbor_name = get_state_string(ni, nj)
                            graph.add_edge(node_name, neighbor_name)

        distance_dict = dict(nx.all_pairs_dijkstra_path_length(graph))
        del graph
        # Begin by iterating through each element of the map_object
        for element in map_object:
            # This is the dictionary that will be attached to each key in the self._reward_matrix
            # Each key corresponds to each element of the map_object.
            result_dict = {}
            location = get_state_string(element[0], element[1])
            # Get the distance dictionary from the state digraph
            element_distance_dict = distance_dict[location]
            # Step value, based on the largest distance to the element
            element_step_value = 1 / max(element_distance_dict.values())

            rows, cols = array.shape
            # Iterate through each cell of the passed array
            for i in range(rows):
                for j in range(cols):
                    # The try catch clause is used, because elements such as rocks are not in the digraph
                    # and will throw a KeyError
                    try:
                        # Get the current cell's distance to the current map object element
                        if is_bottom:
                            cell_key = f"{i + 11},{j}"
                        else:
                            cell_key = f"{i},{j}"

                        # Calculate the reward value
                        cell_distance = distance_dict[cell_key][location]
                        reward_value = 1 - (cell_distance * element_step_value)
                        result_dict[cell_key] = reward_value
                    except KeyError:
                        pass
            # Add the dictionary to the reward matrix using the element as the key name
            self._reward_matrix[location] = result_dict

    def _get_state(self, location: list) -> int:
        """
        Performs a lookup using the location of the passed cell into the state table, and returns
        the state value as an integer. Used for returning observation information.
        :param location: numpy array of the cell location [row, col]
        :return: Integer representing the state number of the cell
        """
        state = self._state_array[location[0]][location[1]]
        return int(state)

    def _get_tank_reward(self) -> float:
        if self._target is not None:
            tank_name = f"{self._target[0]},{self._target[1]}"
            reward_dict = self._reward_matrix[tank_name]
            reward_to_cur_state = reward_dict[f"{self._agent_location[0]},{self._agent_location[1]}"]
        return reward_to_cur_state

    def render(self):
        """
        This function is used for rendering, and is currently not implemented
        :return: None
        """
        if self.render_mode == "console":
            pass

    def reset(self, seed=None, options=None) -> tuple:
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
        self.map_csv = np.genfromtxt(self._map_name, delimiter=",")
        self._agent_location = np.argwhere(self.map_csv == START)[0]
        self._agent_top = None
        self._target = None
        self._tanks_destroyed = []
        self._tank_list = []
        self.episode_length = 0  # Initialize episode length

        observation = self._get_obs()
        info = self._get_info()
        # with open('/content/trajectories.txt', 'a') as writefile:
        #     writefile.write(f"Reset; {observation}\n")

        return observation, info

    def step(self, action) -> tuple:

        assert action in [0, 1, 2, 3, 4], "Error! Action must be 0, 1, 2, 3, 4"
        reward = 0
        terminated = False
        self.episode_length += 1
        if self.episode_length > 20000:
            terminated = True

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
                            self._tank_list.extend(self._tank_loc_top.tolist())
                            self._get_closest_objective()
                        elif action == 3:
                            self._agent_top = False
                            self._tank_list.extend(self._tank_loc_bottom.tolist())
                            self._get_closest_objective()

                    # Don't allow an exit until all tanks have been destroyed
                    if len(self._tanks_destroyed) == self._tank_count:

                        # An episode is done iff the agent has reached the target
                        if self._agent_top:
                            terminated = np.array_equal(self._agent_location, self._exit_loc_top[0])
                            if terminated:
                                print("Exit Reached")
                                reward = 1000
                        else:
                            terminated = np.array_equal(self._agent_location, self._exit_loc_bottom[0])
                            if terminated:
                                print("Exit Reached")
                                reward = 1000

            reward = self._get_reward()

        # If the action is a weapons fire
        elif action == 4:

            # Determine if there is a tank close by using a distance metric?
            if self._check_radar():
                print("Tank Destroyed")
                reward = 1000
                self._get_closest_objective()

        # Get the information to be returned by the step method for gym
        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info


from locals import state_to_row_col
from locals import coord_to_state


def location_to_string(location: list):
    return f"{location[0]},{location[1]}"


class ExpertAnchorBaseline(FullAnchoringBaseline):
    """
    This class translates the actions undertaken by the human demonstrators, and returns the observation information
    """

    # TODO: UPDATE THE GET OBS FUNCTION TO INCLUDE THE CURRENT TARGET DONKEY
    def __init__(self, map_name: str, expert_data: dict, gamma: float = .99, rho: float = .5):
        """

        :param map_name:
        :param target_list: A list, in order, of the targets that the human destroyed.  This is used to update the
                            target variable in the observation space, and for calculating the reward values.
        :param gamma:
        :param rho: Hyperparameter to offset the reward value if the agent is replicating the human expert behavior
        """
        super().__init__(map_name)
        self._expert_data = expert_data
        self._target_list = list(expert_data["targets"])
        self._target_list_coord = [state_to_row_col[state_code] for state_code in self._target_list]
        self._gamma = gamma
        self._rho = rho
        # Determine if the expert's targets were top or bottom of the map.
        if any(self._target_list_coord) in self._tank_loc_top:
            # If they are on top, then zero out the tank values on the bottom
            for tank in self._tank_loc_bottom:
                self.map_csv[tank[0]][tank[1]] = 0
        else:
            # If they are on the bottom, zero out the tanks on the top
            for tank in self._tank_loc_top:
                self.map_csv[tank[0]][tank[1]] = 0
        self._visited_states = []

    def _get_obs(self) -> dict:
        """
        Returns the observation information of the environment.  Converts the cell location to a state number for
        the agent, the tank locations, and the exit locations.  Returns these values as a dictionary.
        :return:
        """
        # Get the agent's state and the exit state
        agent_state = self._get_state(self._agent_location)
        if self._agent_top is None:
            exit_state = self._size  # Null value
            tank_states = [self._size for _ in range(self._tank_count)]
        elif self._agent_top:
            exit_state = self._get_state(self._exit_loc_top[0])
            tank_states = []
            for tank in self._tank_list:
                tank_states.append(self._get_state(tank))
        elif not self._agent_top:
            exit_state = self._get_state(self._exit_loc_bottom[0])
            tank_states = []
            for tank in self._tank_list:
                tank_states.append(self._get_state(tank))
        else:
            exit_state = self._size  # Null value
            tank_states = [self._size for _ in range(self._tank_count)]

        target_state = self._target_list[0]

        return np.array([int(agent_state), int(target_state), int(exit_state)], dtype=int)

    def step(self, action) -> tuple:

        assert action in [0, 1, 2, 3, 4], "Error! Action must be 0, 1, 2, 3, 4"
        reward = -.01
        terminated = False
        obs = list(self._get_obs())
        self.episode_length += 1
        if self.episode_length > 20000:
            terminated = True

        for items in self._expert_data["data"]:
            if obs == items[0]:
                if action == items[1]:
                    reward = 1

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
                            self._tank_list.extend(self._tank_loc_top.tolist())
                            self._get_closest_objective()
                        elif action == 3:
                            self._agent_top = False
                            self._tank_list.extend(self._tank_loc_bottom.tolist())
                            self._get_closest_objective()

                    """
                    target_idx = state_to_row_col[int(self._target_list[0])]
                    target_idx = location_to_string(target_idx)
                    try:
                        reward = self._reward_matrix[target_idx][location_to_string(self._agent_location)]
                    except KeyError:
                        reward = 0


                    # Calculate the F value.  If the state is a state from the expert data, and the actions match,
                    # then it's just the reward value.  If the actions do not match the f value is 0.  If the states
                    # to do not match, it's the f value calculation
                    if use_f_value:
                        f = (self._gamma * state_prime_potential) - state_potential
                        print(f"F value: {f}")
                        print(f"Old reward: {reward}")
                        reward += f
                        print(f"New Reward:{reward}")
                    """

                    # Don't allow an exit until all tanks have been destroyed
                    if len(self._tanks_destroyed) == self._tank_count:

                        # An episode is done iff the agent has reached the target
                        if self._agent_top:
                            terminated = np.array_equal(self._agent_location, self._exit_loc_top[0])
                            if terminated:
                                print("Exit Reached")
                                reward = 1000
                        else:
                            terminated = np.array_equal(self._agent_location, self._exit_loc_bottom[0])
                            if terminated:
                                print("Exit Reached")
                                reward = 1000

        # If the action is a weapons fire
        elif action == 4:

            # Determine if there is a tank close by using a distance metric?
            # TODO: FIX THIS SO THERE IS NO REWARD FOR DESTROYING TANKS OFF MAP
            if self._check_radar():
                print("Tank Destroyed")
                reward = 1000
                self._get_closest_objective()
                self._target_list.pop(0)

        # Get the information to be returned by the step method for gym
        observation = self._get_obs()
        info = self._get_info()
        # print(observation, action, reward)
        return observation, reward, terminated, False, info

    def reset(self, seed=None, options=None) -> tuple:
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
        self.map_csv = np.genfromtxt(self._map_name, delimiter=",")
        self._agent_location = np.argwhere(self.map_csv == START)[0]
        self._agent_top = None
        self._target = None
        self._tanks_destroyed = []
        self._tank_list = []
        self.episode_length = 0  # Initialize episode length
        self._target_list = list(self._expert_data["targets"])
        self._target_list_coord = [state_to_row_col[int(state_code)] for state_code in self._target_list]
        self._expert_data = self._expert_data

        observation = self._get_obs()
        info = self._get_info()
        # with open('/content/trajectories.txt', 'a') as writefile:
        #     writefile.write(f"Reset; {observation}\n")

        return observation, info


from anch_human_demonstr import par1_cond1
