from typing import List

import numpy as np
from scipy import interpolate

from skimage.filters import gaussian
from skimage.segmentation import active_contour


def add_node(event, nodes, canvas):
    nodes.append((event.xdata, event.ydata))
    event.inaxes.plot([event.xdata], [event.ydata], marker="o", color="r")
    canvas.draw()


def spline(nodes: np.ndarray, resolution=360, degree=3) -> np.ndarray:
    """Returns a spline that passes through the given points."""
    data = np.vstack((nodes, nodes[0]))
    tck, u = interpolate.splprep([data[:, 0], data[:, 1]], s=0, per=True, k=degree)[:2]
    return np.array(interpolate.splev(np.linspace(0, 1, resolution), tck)).T


def segment_one_image(image, nodes, sigma=1, resolution=360, degree=3, **kwargs):
    initial = spline(np.array(nodes), resolution=resolution, degree=degree)
    fimg = gaussian(image, sigma=sigma)
    return active_contour(fimg, initial, **kwargs)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from skimage.io import imread

    # First we load the image and transform it to greyscale
    img = imread("beetles.jpg", as_gray=True)

    # Variable to accumulate the nodes
    nodes: List = []

    # We plot it and pick the initial contour. To finish picking nodes, close the figure
    fig = plt.figure()
    fig.canvas.mpl_connect(
        "button_release_event", lambda event: add_node(event, nodes, fig.canvas)
    )
    ax = fig.add_subplot()
    ax.imshow(img, cmap=plt.get_cmap("binary_r"))
    plt.show()

    # Create the spline, filter the image and run the segmentation
    silhouette = segment_one_image(img, nodes)

    # Finally, we plot the result
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.imshow(img, cmap=plt.get_cmap("binary_r"))
    ax.plot(*silhouette.T)
    plt.show()

    # And potentially save the data
    # import numpy as np
    # np.savetxt("silhouette.txt", silhouette)
