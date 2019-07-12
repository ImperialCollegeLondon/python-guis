import matplotlib.pyplot as plt

from python_guis import figure_actions_manager as fam
from skimage.filters import gaussian
from skimage.io import imread
from skimage.segmentation import active_contour

# First we load the image and transform it to greyscale
img = imread("beetles.jpg", as_gray=True)

# We plot it and pick the initial contour
fig = plt.figure()
actions = fam.FigureActionsManager(
    fig,
    fam.DrawContours,
    axis_fraction=0,
    options_DrawContours={"num_contours": 1, "num_points": 6},
)
ax = fig.add_subplot()
ax.imshow(img, cmap=plt.get_cmap("binary_r"))
plt.show()

# After closing the figure, we retrieve the contour data from the figure actions manager
initial = list(actions.DrawContours.contour_data.values())[0][0]

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
