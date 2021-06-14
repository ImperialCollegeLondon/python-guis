import tkinter as tk
from tkinter import ttk
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from python_guis import INSECTS
from python_guis.model import add_node, segment_one_image
from skimage.io import imread


class BeetlePicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beetle Picker")

        self.filename = ""
        self.image = None
        self.nodes = []

        # gui variables
        self.sigma_scale = tk.IntVar(value=1)
        self.sigma_label = tk.StringVar(value=1)
        self.spline_resolution = tk.IntVar(value=360)
        self.spline_degree = tk.IntVar(value=3)
        self.segment_button = None
        self.remove_all_segments_button = None
        self.fig = None
        self.axes = None

        # create the GUI
        self.create_gui()

        # read image
        self.read_image()

    def create_gui(self):
        """Creates the widgets and link them to the GUI variables."""
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # The plot
        self.fig = Figure(tight_layout=True)
        self.axes = self.fig.add_subplot()
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(column=1, row=0, sticky=tk.NSEW)

        # The main frame, which will hold all the widgets except the plot
        mainframe = ttk.Frame(self, width=300)
        mainframe.grid(column=0, row=0, sticky=tk.NSEW, ipadx=15, ipady=15)
        mainframe.columnconfigure(1, weight=1)

        # Gaussian filter
        ttk.Label(mainframe, text="Gaussian filter width: ").grid(
            row=1, columnspan=2, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Label(mainframe, textvariable=self.sigma_label).grid(
            row=2, sticky=tk.E, padx=5, pady=5
        )
        ttk.Scale(
            mainframe,
            orient=tk.HORIZONTAL,
            from_=0,
            to=10,
            variable=self.sigma_scale,
            command=lambda *args: self.sigma_label.set(self.sigma_scale.get()),
        ).grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)

        # Spline
        ttk.Label(mainframe, text="Spline parameters: ").grid(
            row=3, columnspan=2, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Label(mainframe, text="- Degree:").grid(
            row=4, sticky=tk.NSEW, padx=5, pady=5
        )
        degree_frame = ttk.Frame(mainframe)
        degree_frame.grid(row=4, column=1, sticky=tk.NSEW)
        for i in [1, 3, 5]:
            degree_frame.columnconfigure((i - 1) // 2, weight=1)
            ttk.Radiobutton(
                degree_frame, text=i, value=i, variable=self.spline_degree
            ).grid(row=0, column=(i - 1) // 2, sticky=tk.NSEW)
        ttk.Label(mainframe, text="- Resolution:").grid(
            row=5, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Entry(mainframe, textvariable=self.spline_resolution).grid(
            row=5, column=1, sticky=tk.NSEW, padx=5, pady=5
        )

        # Perform segmentation
        self.segment_button = ttk.Button(
            mainframe,
            text="Perform segmentation",
            command=self.perform_segmentation,
            state=tk.DISABLED,
        )
        self.segment_button.grid(row=6, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # Remove data
        self.remove_all_segments_button = ttk.Button(
            mainframe,
            text="Remove all",
            command=self.remove_all_segmentations,
            state=tk.DISABLED,
        )
        self.remove_all_segments_button.grid(
            row=7, columnspan=2, sticky=(tk.S, tk.W, tk.E), padx=5, pady=5
        )

    def remove_all_segmentations(self):
        """Removes all segmentations from memory."""
        self.nodes = []
        self.remove_all_segments_button.configure(state=tk.DISABLED)
        self.axes.lines.clear()
        self.axes.get_legend().remove()
        self.fig.canvas.draw()

    def add_node(self, event):
        """Adds a node to the plot."""
        if len(self.nodes) == 0:
            self.axes.lines.clear()

        add_node(event, self.nodes, self.fig.canvas)

        if len(self.nodes) >= 3:
            self.segment_button.configure(state=tk.NORMAL)

    def redraw(self, segment=None, initial=None):
        """Redraws the axes after making a changes to the data."""

        if initial is not None:
            self.axes.plot(*initial.T, color="blue", label="Initial")

        if segment is not None:
            self.axes.plot(*segment.T, color="orange", label="Segmented")

        if segment is not None or initial is not None:
            self.axes.legend()

        self.fig.canvas.draw()

    def draw(self):
        """Initial drawing of the plot."""
        self.axes.imshow(self.image, cmap=plt.get_cmap("binary_r"))
        self.axes.set_title(
            "Left click to add a control node.\n"
            "At least 3 are needed to perform a segmentation."
        )

    def perform_segmentation(self):
        """Gets all the parameters from the widgets and performs the segmentation."""
        sigma = self.sigma_scale.get()
        resolution = self.spline_resolution.get()
        degree = self.spline_degree.get()

        segment, initial = segment_one_image(
            self.image, self.nodes, sigma=sigma, resolution=resolution, degree=degree
        )

        self.remove_all_segments_button.configure(state=tk.NORMAL)
        self.segment_button.configure(state=tk.DISABLED)

        self.nodes = []
        self.redraw(segment, initial)

    def read_image(self, *args):
        """Opens the image to segment."""
        self.image = imread(INSECTS, as_gray=True)
        self.draw()
        self.fig.canvas.mpl_connect("button_release_event", self.add_node)


if __name__ == "__main__":
    BeetlePicker().mainloop()
