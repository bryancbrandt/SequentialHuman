# Define the path to the log file
log_file_path = 'participant30.log'

# Initialize a flag to keep track of the last keyword found
last_keyword = None

# Open the log file and read its content
try:
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            # Check if the line contains ":MapName" and ":Exit Chosen:"
            if ":MapName" in line:
                print(line.strip())
            elif ":Exit Chosen:" in line:
                print(line.strip())
                print()
except FileNotFoundError:
    print(f"File not found: {log_file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

print()
print()

# Initialize a flag to indicate whether to print the next three lines
print_next_three_lines = 0

# Open the log file and read its content
try:
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            # Check if the line contains "AnchorBaseline:MapName:"
            if "AnchorBaseline:MapName:" in line:
                print(line.strip())  # Print the line containing the keyword
                print_next_three_lines = 3  # Set the flag to print the next three lines

            # Check if we should print the next line
            if print_next_three_lines > 0:
                print(line.strip())
                print_next_three_lines -= 1

except FileNotFoundError:
    print(f"File not found: {log_file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

