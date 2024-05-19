import os
import sys
import time
from resource import *

import psutil


class basic_dna_alignment:
    def __init__(self):
        self.gap_cost = 30
        self.mismatch_cost = {
            "A": {"A": 0, "C": 110, "G": 48, "T": 94},
            "C": {"A": 110, "C": 0, "G": 118, "T": 48},
            "G": {"A": 48, "C": 118, "G": 0, "T": 110},
            "T": {"A": 94, "C": 48, "G": 110, "T": 0},
        }

    def calculate_cost_of_alignment(self, s1, s2):
        m = len(s1) + 1
        n = len(s2) + 1
        opt = [[float("inf")] * n for _ in range(m)]

        opt[0][0] = 0
        for i in range(1, m):
            opt[i][0] = i * self.gap_cost
        for j in range(1, n):
            opt[0][j] = j * self.gap_cost

        for i in range(1, m):
            for j in range(1, n):
                opt[i][j] = min(
                    opt[i - 1][j - 1] + self.mismatch_cost[s1[i - 1]][s2[j - 1]],
                    min(opt[i - 1][j] + self.gap_cost, opt[i][j - 1] + self.gap_cost),
                )

        return opt, opt[m - 1][n - 1]

    def generate_dna_alignment(self, opt, s1, s2):
        i, j = len(s1), len(s2)
        opt_alignment_s1 = ""
        opt_alignment_s2 = ""
        while i > 0 or j > 0:
            if (
                i > 0
                and j > 0
                and opt[i][j]
                == opt[i - 1][j - 1] + self.mismatch_cost[s1[i - 1]][s2[j - 1]]
            ):
                opt_alignment_s1 = s1[i - 1] + opt_alignment_s1
                opt_alignment_s2 = s2[j - 1] + opt_alignment_s2
                i -= 1
                j -= 1
            elif i > 0 and opt[i][j] == opt[i - 1][j] + self.gap_cost:
                opt_alignment_s1 = s1[i - 1] + opt_alignment_s1
                opt_alignment_s2 = "_" + opt_alignment_s2
                i -= 1
            elif j > 0 and opt[i][j] == opt[i][j - 1] + self.gap_cost:
                opt_alignment_s1 = "_" + opt_alignment_s1
                opt_alignment_s2 = s2[j - 1] + opt_alignment_s2
                j -= 1

        while i > 0:
            opt_alignment_s1 = opt_alignment_s1 + s1[i - 1]
            opt_alignment_s2 = opt_alignment_s2 + "_"
            i -= 1
        while j > 0:
            opt_alignment_s1 = opt_alignment_s1 + "_"
            opt_alignment_s2 = opt_alignment_s2 + s2[j - 1]
            j -= 1

        return opt_alignment_s1, opt_alignment_s2


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def generateString(initialString, index):
    if index < len(initialString) + 1:
        modifiedstring = initialString[:index] + initialString + initialString[index:]
    return modifiedstring


try:
    if len(sys.argv) < 3:
        print("Please enter the input file path and output file path")
        sys.exit(1)

    inFilePath = sys.argv[1]
    opFilePath = sys.argv[2]

    with open(inFilePath, "r") as file:
        lines = file.readlines()

    generatedString = ""
    generatedStringArray = []
    for line in lines:
        line = line.strip()
        if line.isalpha():
            if generatedString:
                generatedStringArray.append(generatedString)
            generatedString = line
        else:
            index = int(line)
            generatedString = generateString(generatedString, index + 1)
    if generatedString:
        generatedStringArray.append(generatedString)

        start_time = time.time()

        basic_dna_alignment_obj = basic_dna_alignment()
        opt, opt_alignment_cost = basic_dna_alignment_obj.calculate_cost_of_alignment(
            generatedStringArray[0], generatedStringArray[1]
        )
        opt_aligned_string1, opt_aligned_string2 = (
            basic_dna_alignment_obj.generate_dna_alignment(
                opt, generatedStringArray[0], generatedStringArray[1]
            )
        )
        output_file_path = os.path.join(opFilePath)

        end_time = time.time()
        time_taken = (end_time - start_time) * 1000
        with open(output_file_path, "w") as output_file:
            output_file.write(f"{opt_alignment_cost}\n")
            output_file.write(opt_aligned_string1 + "\n")
            output_file.write(opt_aligned_string2 + "\n")
            output_file.write(str(time_taken) + "\n")
            output_file.write(str(process_memory()) + "\n")

except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Unexpected error occured: {e}")
