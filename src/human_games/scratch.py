"""
state = 0
for i in range(20):
    for j in range(20):
        print(f" {state} : [{i},{j}],")
        state += 1
"""

# Randomization with counter balancing for each anchoring baseline condition
# Generate an array between 1 and 10 in random order
# Then for each one, generate a 1 or a 2 to double it which will flip the map
# This way each participant sees each of the 10 maps, the top/bottom ordering will
# be different though
import numpy as np

rng = np.random.default_rng()

current_list = []
particpant_list = []

while len(particpant_list) < 41:

    while len(current_list) < 10:
        rand = rng.integers(1, 11, size=1)[0]
        if rand not in current_list:
            current_list.append(rand)

    new_list = []
    for items in current_list:
        rand = rng.integers(1, 3, size=1)[0]
        if rand == 2:
            new_list.append(items + 10)
        else:
            new_list.append(items)

    if new_list not in particpant_list:
        particpant_list.append(new_list)
        current_list = []

print(particpant_list)
