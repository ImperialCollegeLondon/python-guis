import os
import tkinter as tk
import tkinter.filedialog
from collections import OrderedDict
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from python_guis.model import add_node, segment_one_image
from skimage.io import imread


class BeetlePicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beetle Picker")
        self.minsize(1280, 720)

        self.filename = ""
        self.image = None
        self.segments = OrderedDict()
        self.nodes = []

        # gui variables
        self.sigma_scale = tk.IntVar(value=1)
        self.sigma_label = tk.StringVar(value=1)
        self.ac_alpha = tk.DoubleVar(value=0.01)
        self.ac_beta = tk.DoubleVar(value=0.1)
        self.ac_gamma = tk.DoubleVar(value=0.01)
        self.spline_resolution = tk.IntVar(value=360)
        self.spline_degree = tk.IntVar(value=3)
        self.beetle_id = tk.StringVar(value="beetle")
        self.available_segmentations = None
        self.segment_button = None
        self.remove_point_button = None
        self.remove_all_segments_button = None
        self.remove_segment_button = None
        self.save_segments_button = None
        self.fig = None
        self.axes = None

        # create the GUI
        self.create_gui()

    def create_gui(self):
        """Creates the widgets and link them to the GUI variables."""
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # The plot and navigation toolbar.
        self.fig = Figure()
        self.axes = self.fig.add_subplot()
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(column=1, row=0, sticky=tk.NSEW)

        # The main frame, which will hold all the widgets except the plot
        mainframe = ttk.Frame(self, width=300)
        mainframe.grid(column=0, row=0, sticky=tk.NSEW, ipadx=15, ipady=15)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(30, weight=1)
        mainframe.rowconfigure(50, weight=2)

        # Read filename
        ttk.Button(mainframe, text="Read image", command=self.read_image).grid(
            row=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5
        )

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

        # active contour
        ttk.Label(mainframe, text="Active contour parameters: ").grid(
            row=7, columnspan=2, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Label(mainframe, text="- Alpha:").grid(
            row=8, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Entry(mainframe, textvariable=self.ac_alpha).grid(
            row=8, column=1, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Label(mainframe, text="- Beta:").grid(row=9, sticky=tk.NSEW, padx=5, pady=5)
        ttk.Entry(mainframe, textvariable=self.ac_beta).grid(
            row=9, column=1, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Label(mainframe, text="- Gamma:").grid(
            row=10, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Entry(mainframe, textvariable=self.ac_gamma).grid(
            row=10, column=1, sticky=tk.NSEW, padx=5, pady=5
        )

        # Perform segmentation
        self.segment_button = ttk.Button(
            mainframe,
            text="Perform segmentation",
            command=self.perform_segmentation,
            state=tk.DISABLED,
        )
        self.segment_button.grid(row=40, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        ttk.Label(mainframe, text="Beetle ID:").grid(
            row=41, sticky=tk.NSEW, padx=5, pady=5
        )
        ttk.Entry(mainframe, textvariable=self.beetle_id).grid(
            row=41, column=1, sticky=tk.NSEW, padx=5, pady=5
        )

        # Remove data
        ttk.Label(mainframe, text="Remove:").grid(
            row=46, sticky=tk.NSEW, padx=5, pady=5
        )
        self.remove_point_button = ttk.Button(
            mainframe,
            text="Last point",
            command=self.remove_last_point,
            state=tk.DISABLED,
        )
        self.remove_point_button.grid(row=47, sticky=(tk.S, tk.W, tk.E), padx=5, pady=5)
        self.remove_segment_button = ttk.Button(
            mainframe,
            text="Last segment",
            command=self.remove_last_segmentation,
            state=tk.DISABLED,
        )
        self.remove_segment_button.grid(
            row=48, sticky=(tk.S, tk.W, tk.E), padx=5, pady=5
        )
        self.remove_all_segments_button = ttk.Button(
            mainframe,
            text="Remove all",
            command=self.remove_all_segmentations,
            state=tk.DISABLED,
        )
        self.remove_all_segments_button.grid(
            row=49, sticky=(tk.S, tk.W, tk.E), padx=5, pady=5
        )

        # Available segmentations
        self.available_segmentations = tk.Text(mainframe, width=25)
        self.available_segmentations.grid(
            row=46, column=1, rowspan=10, sticky=tk.NSEW, padx=5, pady=5
        )

        # Save segmentations
        self.save_segments_button = ttk.Button(
            mainframe,
            text="Save segmentations",
            command=self.save_segmentations,
            state=tk.DISABLED,
        )
        self.save_segments_button.grid(
            row=91, columnspan=2, sticky=(tk.S, tk.W, tk.E), padx=5, pady=5
        )

    def remove_all_segmentations(self):
        """Removes all segmentations from memory."""
        self.segments = OrderedDict()
        self.nodes = []
        self.remove_point_button["state"] = tk.DISABLED
        self.remove_segment_button["state"] = tk.DISABLED
        self.remove_all_segments_button["state"] = tk.DISABLED
        self.save_segments_button["state"] = tk.DISABLED
        self.available_segmentations.delete("1.0", tk.END)
        self.redraw()

    def remove_last_segmentation(self):
        """Removes the last segmentation from memory."""
        self.segments.popitem()
        self.redraw()

        if len(self.segments) == 0:
            self.remove_segment_button["state"] = tk.DISABLED
            self.remove_all_segments_button["state"] = tk.DISABLED
            self.save_segments_button["state"] = tk.DISABLED

    def remove_last_point(self):
        """Removes last node drawn."""
        if len(self.nodes) > 0:
            self.nodes.pop(-1)
            self.redraw()

        if len(self.nodes) == 0:
            self.remove_point_button["state"] = "disable"

    def add_node(self, event):
        """Adds a node to the plot."""
        add_node(event, self.nodes, self.fig.canvas)
        if len(self.nodes) > 0:
            self.remove_point_button["state"] = tk.NORMAL
        if len(self.nodes) >= 3:
            self.segment_button["state"] = tk.NORMAL

    def add_segmentation_to_list(self, name, data, idx=0):
        """Adds a new segmentation to the list."""
        if name in self.segments:
            new = name + str(idx)
            self.add_segmentation_to_list(new, data, idx=idx + 1)
        else:
            self.segments[name] = data
            self.available_segmentations.insert(tk.END, name + "\n")

    def redraw(self):
        """Redraws the axes after making a changes to the data."""
        self.axes.clear()
        self.available_segmentations.delete("1.0", tk.END)

        if self.image is not None:
            self.axes.imshow(self.image, cmap=plt.get_cmap("binary_r"))
            self.axes.set_title(
                "Left click to add a control node.\n"
                "At least 3 are needed to perform a segmentation."
            )

        for k, value in self.segments.items():
            self.axes.plot(*value[0].T)
            self.available_segmentations.insert(tk.END, k + "\n")

        for n in self.nodes:
            self.axes.plot(n[0], n[1], marker="o", color="r")

        self.fig.canvas.draw()

    def perform_segmentation(self):
        """Gets all the parameters from the widgets and performs the segmentation."""
        sigma = self.sigma_scale.get()
        resolution = self.spline_resolution.get()
        degree = self.spline_degree.get()
        alpha = self.ac_alpha.get()
        beta = self.ac_beta.get()
        gamma = self.ac_gamma.get()
        name = self.beetle_id.get()

        segment = segment_one_image(
            self.image,
            self.nodes,
            sigma=sigma,
            resolution=resolution,
            degree=degree,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
        )

        self.nodes = []
        self.add_segmentation_to_list(name, segment)

        self.remove_point_button["state"] = tk.DISABLED
        self.remove_segment_button["state"] = tk.NORMAL
        self.remove_all_segments_button["state"] = tk.NORMAL
        self.save_segments_button["state"] = tk.NORMAL
        self.segment_button["state"] = tk.DISABLED

        self.redraw()

    def read_image(self, *args):
        """Opens a filedialog to choose the image to segment."""
        self.filename = tk.filedialog.askopenfilename(
            filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png"))
        )

        if self.filename != "":
            self.image = imread(self.filename, as_gray=True)
            self.redraw()
            self.fig.canvas.mpl_connect("button_release_event", self.add_node)

    def save_segmentations(self):
        """Saves the available segmentations in a txt file."""
        path = tk.filedialog.askdirectory(title="Select Destination directory")

        if path != "":
            for k, value in self.segments.items():
                filename = os.path.join(path, k + ".txt")
                np.savetxt(filename, value)


if __name__ == "__main__":
    BeetlePicker().mainloop()
