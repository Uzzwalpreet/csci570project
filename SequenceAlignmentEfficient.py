from collections import defaultdict
import sys
import os


class SequenceAlignmentMemoryEfficient:
    def __init__(self):
        self.gap_penalty = 30
        self.mismatch_penalty_table = defaultdict(lambda: defaultdict(int))
        self.initialize_penalty_table()

    def initialize_penalty_table(self):
        self.mismatch_penalty_table['A']['A'] = 0
        self.mismatch_penalty_table['A']['C'] = 110
        self.mismatch_penalty_table['A']['G'] = 48
        self.mismatch_penalty_table['A']['T'] = 94
        self.mismatch_penalty_table['C']['A'] = 110
        self.mismatch_penalty_table['C']['C'] = 0
        self.mismatch_penalty_table['C']['G'] = 118
        self.mismatch_penalty_table['C']['T'] = 48
        self.mismatch_penalty_table['G']['A'] = 48
        self.mismatch_penalty_table['G']['C'] = 118
        self.mismatch_penalty_table['G']['G'] = 0
        self.mismatch_penalty_table['G']['T'] = 110
        self.mismatch_penalty_table['T']['A'] = 94
        self.mismatch_penalty_table['T']['C'] = 48
        self.mismatch_penalty_table['T']['G'] = 110
        self.mismatch_penalty_table['T']['T'] = 0

    def compute_minimum_alignment_cost(self, s1, s2):

        m = len(s1) + 1
        n = len(s2) + 1
        opt = [[sys.maxsize] * n for _ in range(m)]

        # Initialize edge case
        opt[0][0] = 0
        for i in range(1, m):
            opt[i][0] = i * self.gap_penalty
        for i in range(1, n):
            opt[0][i] = i * self.gap_penalty

        # DP formula bottom-up
        for i in range(1, m):
            for j in range(1, n):
                opt[i][j] = min(opt[i - 1][j - 1] + self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]],
                                opt[i - 1][j] + self.gap_penalty,
                                opt[i][j - 1] + self.gap_penalty)

        return opt[m][n]

    def reconstruct_alignment(self, table, s1, s2):
        i = len(table) - 1
        j = len(table[0]) - 1

        alignment_s1 = ""
        alignment_s2 = ""
        while i > 0 or j > 0:
            if j > 0 and table[i][j] == (table[i][j - 1] + self.gap_penalty):
                alignment_s1 = '_' + alignment_s1
                alignment_s2 = s2[j - 1] + alignment_s2
                j -= 1
            elif i > 0 and j > 0 and table[i][j] == (table[i - 1][j - 1] + self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]]):
                alignment_s1 = s1[i - 1] + alignment_s1
                alignment_s2 = s2[j - 1] + alignment_s2
                i -= 1
                j -= 1
            elif i > 0 and table[i][j] == (table[i - 1][j] + self.gap_penalty):
                alignment_s1 = s1[i - 1] + alignment_s1
                alignment_s2 = '_' + alignment_s2
                i -= 1

        return alignment_s1, alignment_s2

    def divide_and_conquer_alignment(self, s1, s2):
        if len(s1) <= 2 or len(s2) <= 2:
            opt_table = self.compute_minimum_alignment_cost(s1, s2)
            return self.reconstruct_alignment(opt_table, s1, s2)

        res = []

        s1_mid = len(s1) // 2
        if s1_mid < 1:  # Ensure left part has at least one character
            s1_mid = 1
        s1_left_part = s1[:s1_mid]
        print("The s1 left part is:", s1_left_part)

        cost_left = self.space_efficient_alignment(s1_left_part, s2)

        s1_right_part = s1[s1_mid:]
        reversed_s1_right_part = s1_right_part[::-1]
        reversed_s2 = s2[::-1]
        cost_right = self.space_efficient_alignment(
            reversed_s1_right_part, reversed_s2)

        print("The cost of left part is:", cost_left)
        print("The cost of right part is:", cost_right)

        cost = [left + right for left,
                right in zip(cost_left, reversed(cost_right))]

        s2_optimal_divide_length = cost.index(min(cost))
        opt_value = cost[s2_optimal_divide_length]

        res_left = self.divide_and_conquer_alignment(
            s1_left_part, s2[:s2_optimal_divide_length])
        res_right = self.divide_and_conquer_alignment(
            s1_right_part, s2[s2_optimal_divide_length:])

        res.extend(res_right[::-1])
        res.extend(res_left[::-1])

        print("The opt is", opt_value)
        return opt_value, res

    def space_efficient_alignment(self, s1, s2):
        m = len(s1) + 1
        n = len(s2) + 1
        table = [[sys.maxsize] * n for _ in range(2)]

        for i in range(n):
            table[0][i] = i * self.gap_penalty

        for i in range(1, m):
            table[1][0] = i * self.gap_penalty
            for j in range(1, n):
                table[1][j] = min(table[0][j - 1] + self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]],
                                  table[0][j] + self.gap_penalty,
                                  table[1][j - 1] + self.gap_penalty)
            table[0] = table[1]

        return table[1]


def modify_string(base_string, index):
    if index < len(base_string)+1:
        new_string = base_string[:index] + base_string + base_string[index:]
    else:
        # If index is out of bounds, append at the end
        new_string = base_string + base_string

    return new_string

# Example usage:


try:
    with open("Project 2/SampleTestCases/input2.txt", "r") as file1:
        lines = file1.readlines()

    current_string = ""
    output_string = ""
    arr = []
    for line in lines:
        line = line.strip()  # Remove any extra whitespace or newline characters
        if line.isalpha():  # This line is a new string
            if current_string:  # If there's a current string being processed

                # Append the final output of the current string to the array
                arr.append(output_string)
            current_string = line  # Set new current string
            output_string = current_string  # Reset output string to current string
        else:  # This line is an index
            index = int(line)
            output_string = modify_string(output_string, index+1)

    # After finishing all lines, append the last processed string
    if current_string:

        arr.append(output_string)
        aligner = SequenceAlignmentMemoryEfficient()
        print("The array is", arr[0], arr[1])
        opt_value, alignment = aligner.divide_and_conquer_alignment(
            arr[0], arr[1])
        print("The opt value is ", opt_value)
        # print("The output is", opt_value, alignment)
        # aligns1, aligns2 = aligner.reconstruct_alignment(opt, arr[0], arr[1])
        # output_file_path = os.path.join(
        #     "Project 2", "SampleTestCases", "output2final.txt")

        # with open(output_file_path, "w") as output_file:
        #     output_file.write(f"{alignment_cost}\n")
        #     output_file.write(aligns1 + "\n")
        #     output_file.write(aligns2 + "\n")

except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")


# aligner = SequenceAlignment()
# s1 = "AGTACGCA"
# s2 = "TATGC"
# opt_value, alignment = aligner.divide_and_conquer_alignment(s1, s2)
# print("Alignment Cost:", opt_value)
# for pair in alignment:
#     print(pair[0], pair[1])
