import matplotlib.pyplot as plt
import numpy as np
 
#basic 
x = [16,64,128,256,384,512,768,1024,1280,1536,2048,2560,3072,3584,3968]
y = [14592,14832,14688,15440,16400,17424,20896,25264,31072,38528,56592,79840,108336,141872,170416]
 
# first plot with basic data
plt.plot(x, y, label = "basic", marker='o')

#efficient
x1 = [16,64,128,256,384,512,768,1024,1280,1536,2048,2560,3072,3584,3968]
y1 = [14800,15440,14608,15088,14640,15024,14960,14928,15216,15248,15312,15184,15424,15328,15408]
 
# second plot with x1 and y1 data
plt.plot(x1, y1, label = "efficient", marker='x')
 
plt.xlabel("Length of Input Strings (m+n)")
plt.ylabel("Memory Used in Killobytes")
plt.title('Basic vs Efficient Algo Memory Line Graph')
plt.legend()
plt.show()
