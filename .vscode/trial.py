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
        for j in range(1, n):
            opt[0][j] = j * self.gap_penalty

        # DP formula bottom-up
        for i in range(1, m):
            for j in range(1, n):
                opt[i][j] = min(opt[i - 1][j - 1] + self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]],
                                opt[i - 1][j] + self.gap_penalty,
                                opt[i][j - 1] + self.gap_penalty)

        return opt

    def space_efficient_alignment(self, s1, s2):
        m = len(s1) + 1
        n = len(s2) + 1
        table = [[sys.maxsize] * n for _ in range(2)]

        for j in range(n):
            table[0][j] = j * self.gap_penalty

        for i in range(1, m):
            table[1][0] = i * self.gap_penalty
            for j in range(1, n):
                table[1][j] = min(table[0][j - 1] + self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]],
                                  table[0][j] + self.gap_penalty,
                                  table[1][j - 1] + self.gap_penalty)
            table[0] = table[1][:]

        return table[1]

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
            opt_value = opt_table[-1][-1]
            alignment = self.reconstruct_alignment(opt_table, s1, s2)
            return opt_value, alignment

        s1_mid = len(s1) // 2
        s1_left_part = s1[:s1_mid]
        s1_right_part = s1[s1_mid:]

        cost_left = self.space_efficient_alignment(s1_left_part, s2)
        cost_right = self.space_efficient_alignment(s1_right_part[::-1], s2[::-1])

        cost = [left + right for left, right in zip(cost_left, reversed(cost_right))]
        s2_optimal_divide_length = cost.index(min(cost))

        left_opt_value, left_alignment = self.divide_and_conquer_alignment(
            s1_left_part, s2[:s2_optimal_divide_length])
        right_opt_value, right_alignment = self.divide_and_conquer_alignment(
            s1_right_part, s2[s2_optimal_divide_length:])

        combined_alignment_s1 = left_alignment[0] + right_alignment[0]
        combined_alignment_s2 = left_alignment[1] + right_alignment[1]
        opt_value = left_opt_value + right_opt_value

        return opt_value, (combined_alignment_s1, combined_alignment_s2)


def modify_string(base_string, index):
    if index < len(base_string):
        new_string = base_string[:index] + base_string + base_string[index:]
    else:
        new_string = base_string + base_string
    return new_string


try:
    with open("Project 2/SampleTestCases/input3.txt", "r") as file1:
        lines = file1.readlines()

    current_string = ""
    output_string = ""
    arr = []
    for line in lines:
        line = line.strip()
        if line.isalpha():
            if current_string:
                arr.append(output_string)
            current_string = line
            output_string = current_string
        else:
            index = int(line)
            output_string = modify_string(output_string, index + 1)

    if current_string:
        arr.append(output_string)
        aligner = SequenceAlignmentMemoryEfficient()
        print("The array is", arr[0], arr[1])
        opt_value, alignment = aligner.divide_and_conquer_alignment(
            arr[0], arr[1])
        print(opt_value)
        print(alignment[0])
        print(alignment[1])

except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
