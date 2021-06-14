from typing import List

import numpy as np
from scipy import interpolate

from skimage.filters import gaussian
from skimage.segmentation import active_contour


def add_node(event, nodes, canvas):
    if event.inaxes is not None:
        nodes.append((event.xdata, event.ydata))
        if len(event.inaxes.lines) > 0:
            event.inaxes.lines[0].set_data(np.array(nodes + [nodes[0]]).T)
        else:
            event.inaxes.plot(event.xdata, event.ydata, "ro-", label="Nodes")
        canvas.draw()


def spline(nodes: np.ndarray, resolution=360, degree=3) -> np.ndarray:
    """Returns a spline that passes through the given points."""
    data = np.vstack((nodes, nodes[0]))
    tck, u = interpolate.splprep([data[:, 0], data[:, 1]], s=0, per=True, k=degree)[:2]
    return np.array(interpolate.splev(np.linspace(0, 1, resolution), tck)).T


def segment_one_image(
    image,
    nodes,
    sigma=1,
    resolution=360,
    degree=3,
    alpha=0.001,
    beta=0.1,
    gamma=0.01,
    **kwargs
):
    initial = spline(np.array(nodes), resolution=resolution, degree=degree)
    fimg = gaussian(image, sigma=sigma)
    contour = active_contour(
        fimg, initial[..., ::-1], alpha=alpha, beta=beta, gamma=gamma, **kwargs
    )[..., ::-1]
    return contour, initial


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from skimage.io import imread

    # First we load the image and transform it to greyscale
    img = imread("insects.jpg", as_gray=True)

    # Variable to accumulate the nodes
    nodes: List = []

    # We plot it and pick the initial contour. To finish picking nodes, close the figure
    fig = plt.figure()
    fig.canvas.mpl_connect(
        "button_release_event", lambda event: add_node(event, nodes, fig.canvas)
    )
    ax = fig.add_subplot()
    ax.imshow(img, cmap=plt.get_cmap("binary_r"))
    ax.set_title("Left click to add a control node\n" "Close image to continue.")
    plt.show()

    # Create the spline, filter the image and run the segmentation
    segment, initial = segment_one_image(img, nodes)

    # Finally, we plot the result
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.imshow(img, cmap=plt.get_cmap("binary_r"))
    ax.plot(*segment.T, label="Initial")
    ax.plot(*initial.T, label="Segmented")
    plt.show()

    # And potentially save the data
    # import numpy as np
    # np.savetxt("silhouette.txt", silhouette)
