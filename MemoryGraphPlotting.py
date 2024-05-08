import matplotlib.pyplot as plt
import numpy as np

# basic
x = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1536, 2048, 2560, 3072, 3584, 3968]
y = [
    14352,
    14624,
    14736,
    15344,
    16224,
    17808,
    20544,
    25488,
    31200,
    38240,
    56272,
    79968,
    108432,
    141392,
    170448,
]

# first plot with basic data
plt.plot(x, y, label="basic", marker="o")

# efficient
x1 = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1536, 2048, 2560, 3072, 3584, 3968]
y1 = [
    14848,
    14864,
    14672,
    15104,
    14704,
    14736,
    14848,
    15056,
    15424,
    14816,
    15440,
    15264,
    15328,
    15232,
    15568,
]

# second plot with x1 and y1 data
plt.plot(x1, y1, label="efficient", marker="x")

plt.xlabel("Length of Input Strings (m+n)")
plt.ylabel("Memory Used in Killobytes")
plt.title("Basic vs Efficient Algo Memory Line Graph")
plt.legend()
plt.show()
