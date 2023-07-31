import os
import networkx as nx
import numpy as np


class StateDiGraph:

    def __init__(self, map_csv: str, allowed_values: list):
        assert isinstance(map_csv, str) and os.path.isfile(map_csv), "Error with map name argument!"
        # assert isinstance(expert_csv, str) and os.path.isfile(expert_csv), "Error with expert data argument"
        assert all(isinstance(item, int) for item in allowed_values), "Error! allowed_values must be a list of ints"

        self.map_csv = np.genfromtxt(map_csv, delimiter=",", dtype=int)
        self.allowed_values = allowed_values

        # Get the dimensions of the array
        rows, cols = self.map_csv.shape

        # Create an array of state values
        # state_array = np.arange(0, rows * cols).reshape(rows, cols)

        # Create an empty directed graph
        self.graph = nx.DiGraph()

        # Iterate through the array
        for i in range(rows):
            for j in range(cols):
                cell_value = self.map_csv[i, j]

                # Check if the cell value is in the allowed_values list
                if cell_value in self.allowed_values:
                    # Add the cell value as a node to the graph
                    node_name = f"{i},{j}"
                    self.graph.add_node(node_name, value=cell_value)

                    # Check and add directed edges to neighboring cells
                    neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                    for ni, nj in neighbors:
                        if 0 <= ni < rows and 0 <= nj < cols and self.map_csv[ni, nj] in allowed_values:
                            neighbor_name = f"{ni},{nj}"
                            self.graph.add_edge(node_name, neighbor_name)

        # Create the distance dictionary
        self.distance_dict = dict(nx.all_pairs_dijkstra_path_length(self.graph))


class ExpertStateDiGraph:
    def __init__(self, map_csv: str, allowed_values: list):
        assert isinstance(map_csv, str) and os.path.isfile(map_csv), "Error with map name argument!"
        # assert isinstance(expert_csv, str) and os.path.isfile(expert_csv), "Error with expert data argument"
        assert all(isinstance(item, int) for item in allowed_values), "Error! allowed_values must be a list of ints"

        self.map_csv = np.genfromtxt(map_csv, delimiter=",", dtype=int)
        self.allowed_values = allowed_values

        # Get the dimensions of the array
        rows, cols = self.map_csv.shape

        # Create an array of state values
        state_array = np.arange(0, rows * cols).reshape(rows, cols)

        # Create an empty directed graph
        self.graph = nx.DiGraph()

        # Iterate through the array
        for i in range(rows):
            for j in range(cols):
                cell_value = self.map_csv[i, j]

                # Check if the cell value is in the allowed_values list
                if cell_value in self.allowed_values:
                    # Add the cell value as a node to the graph
                    node_name = state_array[i, j]
                    self.graph.add_node(node_name, value=cell_value)

                    # Check and add directed edges to neighboring cells
                    neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                    for ni, nj in neighbors:
                        if 0 <= ni < rows and 0 <= nj < cols and self.map_csv[ni, nj] in allowed_values:
                            neighbor_name = state_array[ni, nj]
                            self.graph.add_edge(node_name, neighbor_name)

        # Create the distance dictionary
        self.distance_dict = dict(nx.all_pairs_dijkstra_path_length(self.graph))

        """
        # Load the human demonstrator data
        try:
            expert_data = np.load(expert_csv, allow_pickle=True)
        except Exception as e:
            print(f"Error: An unexpected error occurred: {str(e)}")
            traceback.print_exception()
        self.expert_actions = expert_data['actions'].flatten().tolist()
        self.expert_obs = expert_data['obs']
        self.expert_obs = [sublist[0] for sublist in self.expert_obs]
        """


# sdg = StateDiGraph("../human_games/maps/Anchoring_Baseline/anchoring_baseline_urban_bottom_1.csv", [2, 0, 7, 9])
# print(sdg.distance_dict)
