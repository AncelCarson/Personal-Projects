from mpl_toolkits import mplot3d
#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111,projection = '3d')

x = [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6]
y = [1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,8,9,9,9,9,9,9,10,10,10,10,10,10]
z = [19,19,15,16,12,15,9,10,13,7,12,17,22,22,17,15,13,10,18,16,10,14,11,16,16,8,15,7,19,14,14,11,13,7,17,19,12,5,7,13,19,17,18,7,17,19,12,12,0,10,17,17,8,17,0,18,6,15,6,13]

#ax.plot_trisurf(x,y,z, cmap = 'viridis', edgecolor = 'none')
#ax.plot_surface(x,y,z, cmap = 'viridis', edgecolor = 'none')
#ax.contour(x,y,z, cmap = 'viridis')
ax.tricontour(x,y,z)

plt.show()

