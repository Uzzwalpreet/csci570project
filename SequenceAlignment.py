def modify_string(base_string, index):
    if index < len(base_string)+1:
        new_string = base_string[:index] + base_string + base_string[index:]
    else:
        # If index is out of bounds, append at the end
        new_string = base_string + base_string
    print("The new string is:", new_string)
    return new_string


try:
    with open("Project 2/SampleTestCases/input1.txt", "r") as file1:
        lines = file1.readlines()

    current_string = ""
    output_string = ""
    arr = []  # Initialize array to store the final outputs
    for line in lines:
        line = line.strip()  # Remove any extra whitespace or newline characters
        if line.isalpha():  # This line is a new string
            if current_string:  # If there's a current string being processed
                print(f"Output for {current_string}: {output_string}")
                # Append the final output of the current string to the array
                arr.append(output_string)
            current_string = line  # Set new current string
            output_string = current_string  # Reset output string to current string
        else:  # This line is an index
            index = int(line)
            output_string = modify_string(output_string, index+1)

    # After finishing all lines, append the last processed string
    if current_string:
        print(f"Output for {current_string}: {output_string}")

        arr.append(output_string)
    for i in arr:
        print("The length is", len(i))

    print("Final outputs in array:", arr)

except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
