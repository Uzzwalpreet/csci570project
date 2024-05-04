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


# Example usage


# Example usage

        # Ensure s2 is the shorter string to minimize space usage
        print("HERRREEEE")
        if len(s1) < len(s2):
            s1, s2 = s2, s1

        m, n = len(s1), len(s2)
        previous = [j * self.gap_penalty for j in range(n + 1)]
        current = [0] * (n + 1)
        directions = [None] * (n + 1)  # to store directions for backtracking

        # Fill the DP table
        for i in range(1, m + 1):
            current[0] = i * self.gap_penalty
            directions[0] = 'up'
            for j in range(1, n + 1):
                diagonal = previous[j - 1] + \
                    self.mismatch_penalty_table[s1[i - 1]][s2[j - 1]]
                up = previous[j] + self.gap_penalty
                left = current[j - 1] + self.gap_penalty
                if diagonal <= up and diagonal <= left:
                    current[j] = diagonal
                    directions[j] = 'diag'
                elif up < diagonal and up <= left:
                    current[j] = up
                    directions[j] = 'up'
                else:
                    current[j] = left
                    directions[j] = 'left'
            previous, current = current, previous

        # Reconstruct the alignment
        aligned_s1, aligned_s2 = "", ""
        j = n
        while j > 0:
            if directions[j] == 'diag':
                aligned_s1 = s1[m-1] + aligned_s1
                aligned_s2 = s2[j-1] + aligned_s2
                m -= 1
                j -= 1
            elif directions[j] == 'up':
                aligned_s1 = s1[m-1] + aligned_s1
                aligned_s2 = '_' + aligned_s2
                m -= 1
            elif directions[j] == 'left':
                aligned_s1 = '_' + aligned_s1
                aligned_s2 = s2[j-1] + aligned_s2
                j -= 1

        while m > 0:
            aligned_s1 = s1[m-1] + aligned_s1
            aligned_s2 = '_' + aligned_s2
            m -= 1

        return previous[n], aligned_s1, aligned_s2


# Example usage


def modify_string(base_string, index):
    if index < len(base_string)+1:
        new_string = base_string[:index] + base_string + base_string[index:]
    else:
        # If index is out of bounds, append at the end
        new_string = base_string + base_string

    return new_string


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
        aligner = SequenceAlignment()
        opt, alignment_cost = aligner.compute_minimum_alignment_cost(
            arr[0], arr[1])
        aligns1, aligns2 = aligner.reconstruct_alignment(opt, arr[0], arr[1])


except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")


# Example usage
