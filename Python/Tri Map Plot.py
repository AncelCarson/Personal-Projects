# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

"""Generates a topographical map as an image"""

import numpy as np
from matplotlib import cm
from matplotlib import tri
from  matplotlib import pyplot as plt

#-----------------------------------------------------------------------------
# Analytical test function
#-----------------------------------------------------------------------------
def function_z(x_1, y_1):
    """Z given x an y."""
    r1 = np.sqrt((0.5 - x_1)**2 + (0.5 - y_1)**2)
    theta1 = np.arctan2(0.5 - x_1, 0.5 - y_1)
    r2 = np.sqrt((-x_1 - 0.2)**2 + (-y_1 - 0.2)**2)
    theta2 = np.arctan2(-x_1 - 0.2, -y_1 - 0.2)
    z_1 = -(2 * (np.exp((r1 / 10)**2) - 1) * 30. * np.cos(7. * theta1) +
          (np.exp((r2 / 10)**2) - 1) * 30. * np.cos(11. * theta2) +
          0.7 * (x_1**2 + y_1**2))
    # return np.random.randn(400) #Used for random plot generation
    return (np.max(z_1) - z_1) / (np.max(z_1) - np.min(z_1))

#-----------------------------------------------------------------------------
# Creating a Triangulation
#-----------------------------------------------------------------------------
# First create the x and y coordinates of the points.
n_angles = 20
n_radii = 20
min_radius = 0.15
radii = np.linspace(min_radius, 0.95, n_radii)

angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
angles[:, 1::2] += np.pi / n_angles

x = (radii * np.cos(angles)).flatten()
y = (radii * np.sin(angles)).flatten()
print(len(y))
z = function_z(x, y)

# Now create the Triangulation.
# (Creating a Triangulation without specifying the triangles results in the
# Delaunay triangulation of the points.)
triang = tri.Triangulation(x, y)

# Mask off unwanted triangles.
triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1),
                         y[triang.triangles].mean(axis=1))
                < min_radius)

#-----------------------------------------------------------------------------
# Refine data
#-----------------------------------------------------------------------------
refiner = tri.UniformTriRefiner(triang)
tri_refi, z_test_refi = refiner.refine_field(z, subdiv=3)

#-----------------------------------------------------------------------------
# Plot the triangulation and the high-res iso-contours
#-----------------------------------------------------------------------------
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.triplot(triang, lw=0.5, color='white')

levels = np.arange(-5., 5., 0.25)
cmap = cm.get_cmap(name='terrain', lut=None)
ax.tricontourf(tri_refi, z_test_refi, levels=levels, cmap=cmap)
ax.tricontour(tri_refi, z_test_refi, levels=levels,
               colors=['0.25', '0.5', '0.5', '0.5', '0.5'],
               linewidths=[1.0, 0.5, 0.5, 0.5, 0.5])

ax.set_title("High-resolution tricontouring")

plt.show()
