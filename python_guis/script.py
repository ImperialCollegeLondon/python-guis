import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

from skimage.filters import gaussian
from skimage.io import imread
from skimage.segmentation import active_contour

# First we load the image and transform it to greyscale
img = imread("beetles.jpg", as_gray=True)

# Callback function to get the notes for the spline, and the spline
nodes = []


def add_node(event, canvas):
    nodes.append((event.xdata, event.ydata))
    event.inaxes.plot([event.xdata], [event.ydata], marker="o", color="r")
    canvas.draw()


def spline(
    points: np.ndarray, points_per_contour=6, resolution=360, order=3
) -> np.ndarray:
    """Returns a spline that passes through the given points."""
    data = np.vstack((points[-points_per_contour:], points[-points_per_contour]))
    tck, u = interpolate.splprep([data[:, 0], data[:, 1]], s=0, per=True, k=order)[:2]
    data = np.array(interpolate.splev(np.linspace(0, 1, resolution), tck)).T

    return data.T


# We plot it and pick the initial contour
fig = plt.figure()
fig.canvas.mpl_connect(
    "button_release_event", lambda event: add_node(event, fig.canvas)
)
ax = fig.add_subplot()
ax.imshow(img, cmap=plt.get_cmap("binary_r"))
plt.show()

# After closing the figure, we get the spline that passes through the nodes
initial = spline(np.array(nodes))

# Filter the image and run the segmentation
fimg = gaussian(img, sigma=1)
silhouette = active_contour(fimg, initial.T, alpha=0.015, beta=10, gamma=0.001)

# Finally, we plot the result
fig = plt.figure()
ax = fig.add_subplot()
ax.imshow(img, cmap=plt.get_cmap("binary_r"))
ax.plot(*silhouette.T)
plt.show()

# And potentially save the data
# import numpy as np
# np.savetxt("silhouette.txt", silhouette)
