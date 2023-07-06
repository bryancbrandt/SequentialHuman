import csv
import os
import random
import numpy as np

"""
state = 0
for i in range(20):
    for j in range(20):
        print(f" {state} : [{i},{j}],")
        state += 1
"""


def random_number_arrays_with_counterbalance(number_of_arrays: int = 40, min: int = 1,
                                             max: int = 10, length: int = 10) -> None:
    """
    Randomization with counter balancing.  This function generates an array between
    low and high of with a length of length.  If double is true then for each value
    a coin flip is conducted to determine if the value should be added with 10.
    :param number_of_arrays: How many arrays should be generated
    :param min: the minimum value to be randomly created and placed in the array
    :param max: the maximum value to be randomly created and placed in the array
    :param length: the length of each array
    """
    assert max * max > number_of_arrays, "ERROR, impossible to generate! number of participants > max * max"
    increment = 1

    # Generate unique arrays
    unique_arrays = []
    while len(unique_arrays) < number_of_arrays:
        numbers = list(range(min, max + 1, increment))
        random.shuffle(numbers)
        if numbers not in unique_arrays:
            unique_arrays.append(numbers)
    print(len(unique_arrays))
    print(unique_arrays)


def shuffle_true_false(total_count: int = 10):
    # Calculate the count of each value
    true_count = total_count // 2
    false_count = total_count - true_count

    # Generate True values
    true_values = [True] * true_count

    # Generate False values
    false_values = [False] * false_count

    # Combine the lists and shuffle them
    combined_values = true_values + false_values
    random.shuffle(combined_values)

    # Print the generated values
    print(combined_values)


def pair_arrays(*arrays):
    num_arrays = len(arrays)
    array_length = len(arrays[0])

    paired_arrays = []
    for i in range(array_length):
        pair = list(arr[i] for arr in arrays)
        paired_arrays.append(pair)

    return paired_arrays


def parse_log_file(filename):
    target_prefixes = [
        'AnchorBaseline:MapName:',
        # 'RuralTraining:MapName:',
        # 'AnchoringMask:MapName:',
        # 'Urbantraining:MapName:'
    ]
    matched_lines = []

    with open(filename, 'r') as file:
        for line in file:
            for prefix in target_prefixes:
                if line.startswith(prefix):
                    matched_lines.append(line.strip())
                    break  # Move to the next line after finding the prefix
    for line in matched_lines:
        print(line)


def freq_in_file():

    frequency_dict = {}
    for file_number in range(1, 21):
        filename = f"interbias_{file_number}.csv"  # Replace with the actual filename format
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, f"maps/Interbias/{filename}")
        if os.path.exists(file_path):
            data = np.genfromtxt(file_path, delimiter=",")
            count_1 = np.where(data == 1)[0].size
            count_2 = np.where(data == 2)[0].size
            frequency_dict[file_number] = {"FILE": file_path, "TANK": count_1, "JET": count_2}

