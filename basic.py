import os
import sys
from resource import * 
import time
import psutil


class SequenceAlignment:
    def __init__(self):
        self.gap_penalty = 30
        self.mismatch_penalty_table = {}
        self.initialize_penalty_table()

    def initialize_penalty_table(self):
        # Initialize the nested dictionary for mismatch penalties
        chars = ['A', 'C', 'G', 'T']
        for c1 in chars:
            self.mismatch_penalty_table[c1] = {}
            for c2 in chars:
                self.mismatch_penalty_table[c1][c2] = 0

        # Assign mismatch penalties
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
        m = len(s1) + 1  # OPT table's row size
        n = len(s2) + 1  # OPT table's column size
        opt = [[float('inf')] * n for _ in range(m)]

        # Initialize base cases
        opt[0][0] = 0
        for i in range(1, m):
            opt[i][0] = i * self.gap_penalty
        for j in range(1, n):
            opt[0][j] = j * self.gap_penalty

        # Fill the table with the DP formula bottom-up
        for i in range(1, m):
            for j in range(1, n):
                opt[i][j] = min(opt[i - 1][j - 1] + self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]],
                                min(opt[i - 1][j] + self.gap_penalty, opt[i][j - 1] + self.gap_penalty))

        return opt, opt[m-1][n-1]

    def reconstruct_alignment(self, opt, s1, s2):
        i, j = len(s1), len(s2)
        aligned_s1 = ""
        aligned_s2 = ""
        while i > 0 or j > 0:
            if i > 0 and j > 0 and opt[i][j] == opt[i - 1][j - 1] + self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]]:
                aligned_s1 = s1[i - 1] + aligned_s1
                aligned_s2 = s2[j - 1] + aligned_s2
                i -= 1
                j -= 1
            elif i > 0 and opt[i][j] == opt[i - 1][j] + self.gap_penalty:
                aligned_s1 = s1[i - 1] + aligned_s1
                aligned_s2 = '_' + aligned_s2
                i -= 1
            elif j > 0 and opt[i][j] == opt[i][j - 1] + self.gap_penalty:
                aligned_s1 = '_' + aligned_s1
                aligned_s2 = s2[j - 1] + aligned_s2
                j -= 1

        while i > 0:
            aligned_s1 += s1[i - 1]
            aligned_s2 += "_"
            i -= 1
        while j > 0:
            aligned_s1 += "_"
            aligned_s2 += s2[j - 1]
            j -= 1

        return aligned_s1, aligned_s2


def process_memory():
  process = psutil.Process()
  memory_info = process.memory_info()
  memory_consumed = int(memory_info.rss/1024)
  return memory_consumed

def modify_string(base_string, index):
    if index < len(base_string)+1:
        new_string = base_string[:index] + base_string + base_string[index:]
    else:
        # If index is out of bounds, append at the end
        new_string = base_string + base_string

    return new_string

"""
**String Generation Method**
This method reads the input file from a specific location and generate two strings. 
Starting with an input string and followed by appending the string at spcific index location read from the file.
"""
try:
    with open("Project 2/datapoints/in15.txt", "r") as file1:
        lines = file1.readlines()

    generatedString = ""
    arr = []
    for line in lines:
        line = line.strip()  # to remove /n
        if line.isalpha():  
            if generatedString:  #to append the first generated string
                arr.append(generatedString)  
            generatedString = line #to set the second string
        else:  # for appending at particular index block
            index = int(line)
            generatedString = modify_string(generatedString, index+1)

    if generatedString: #append the second generated string
        arr.append(generatedString)
        #time
        start_time = time.time()
        aligner = SequenceAlignment()
        opt, alignment_cost = aligner.compute_minimum_alignment_cost(
            arr[0], arr[1])
        aligns1, aligns2 = aligner.reconstruct_alignment(opt, arr[0], arr[1])
        output_file_path = os.path.join(
            "Project 2", "Output", "basic15.txt")
        print("Combined length of generated string (m+n)", len(arr[0]) + len(arr[1]))
        end_time = time.time()
        time_taken = (end_time - start_time) * 1000
        with open(output_file_path, "w") as output_file:
            output_file.write(f"{alignment_cost}\n")
            output_file.write(aligns1 + "\n")
            output_file.write(aligns2 + "\n")
            output_file.write(str(time_taken) + "\n")
            output_file.write(str(process_memory()) + "\n")


except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
