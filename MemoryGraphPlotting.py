import matplotlib.pyplot as plt
import numpy as np
 
#basic 
x = [16,64,128,256,384,512,768,1024,1280,1536,2048,2560,3072,3584,3968]
y = [14384,14800,14800,14624,14720,14832,14768,14432,15008,14816,14928,14608,14640,14640,14608]
 
# first plot with basic data
plt.plot(x, y)

#efficeint 
x1 = [16,64,128,256,384,512,768,1024,1280,1536,2048,2560,3072,3584,3968]
y1 = []
 
# second plot with x1 and y1 data
#plt.plot(x1, y1, '-.')
 
plt.xlabel("Length of Input Strings (m+n)")
plt.ylabel("Memory Used in Killobytes")
plt.title('Basic vs Effienct Memory Line Graph')
plt.show()
