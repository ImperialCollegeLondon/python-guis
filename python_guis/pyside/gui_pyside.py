import sys

if sys.platform == "darwin":
    # There is an issue with pyside2 and MacOS BigSur. This hack sorts it
    # https://stackoverflow.com/a/64878899/3778792
    import os

    os.environ["QT_MAC_WANTS_LAYER"] = "1"

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt


from python_guis import INSECTS
from python_guis.model import add_node, segment_one_image
from skimage.io import imread


class PlotArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        fig = Figure(tight_layout=True)
        self.axes = fig.add_subplot()
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        self.canvas = FigureCanvasQTAgg(fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)

        self.layout().addWidget(self.canvas)
        self.layout().addWidget(toolbar)

    def draw(self):
        """Redraws the figure, updating its contents."""
        self.canvas.draw()


class Controls(QtWidgets.QWidget):
    def __init__(self):
        super(Controls, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        # Slider widgets
        self.label = QtWidgets.QLabel("")
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.valueChanged.connect(self._set_label)

        # Radiobutton widgets
        self.button_group = QtWidgets.QButtonGroup()
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(QtWidgets.QLabel("- Degree: "))
        for i in [1, 3, 5]:
            rb = QtWidgets.QRadioButton(f"{i}")
            buttons.addWidget(rb)
            self.button_group.addButton(rb)

        self.button_group.buttons()[1].setChecked(True)

        # Resolution widgets
        resolution = QtWidgets.QHBoxLayout()
        resolution.addWidget(QtWidgets.QLabel("- Resolution: "))
        self.resolution_entry = QtWidgets.QLineEdit("360")
        self.resolution_entry.setValidator(QtGui.QIntValidator())
        self.resolution_entry.setAlignment(Qt.AlignRight)
        resolution.addWidget(self.resolution_entry)

        # Buttons
        self.segment_button = QtWidgets.QPushButton("Perform segmentation")
        self.reset_button = QtWidgets.QPushButton("Remove all")

        # Add widgets to the layout
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.slider)
        self.layout().addWidget(QtWidgets.QLabel("Spline parameters: "))
        self.layout().addLayout(buttons)
        self.layout().addLayout(resolution)
        self.layout().addWidget(self.segment_button)
        self.layout().addWidget(self.reset_button)
        self.layout().addStretch(1)

        self._set_label()

    def _set_label(self):
        text = f"Gaussian filter width: {self.gauss_width:10}"
        self.label.setText(text)

    @property
    def gauss_width(self):
        return int(self.slider.value())

    @property
    def degree(self):
        return int(self.button_group.checkedButton().text())

    @property
    def resolution(self):
        return int(self.resolution_entry.text())


class MySimpleGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())

        self.filename = ""
        self.image = None
        self.nodes = []

        self.controls = Controls()
        self.controls.segment_button.clicked.connect(self.perform_segmentation)
        self.controls.reset_button.clicked.connect(self.remove_all_segmentations)
        self.controls.segment_button.setEnabled(False)
        self.controls.reset_button.setEnabled(False)
        self.layout().addWidget(self.controls)

        self.plot = PlotArea()
        self.layout().addWidget(self.plot)

        # read image
        self.read_image()

    def remove_all_segmentations(self):
        """Removes all segmentations from memory."""
        self.nodes = []
        self.controls.reset_button.setEnabled(False)
        self.plot.axes.lines.clear()
        self.plot.axes.get_legend().remove()
        self.plot.draw()

    def add_node(self, event):
        """Adds a node to the plot."""
        if len(self.nodes) == 0:
            self.plot.axes.lines.clear()

        add_node(event, self.nodes, self.plot.canvas)

        self.controls.reset_button.setEnabled(True)
        if len(self.nodes) >= 3:
            self.controls.segment_button.setEnabled(True)

    def redraw(self, segment=None, initial=None):
        """Redraws the axes after making a changes to the data."""

        if initial is not None:
            self.plot.axes.plot(*initial.T, color="blue", label="Initial")

        if segment is not None:
            self.plot.axes.plot(*segment.T, color="orange", label="Segmented")

        if segment is not None or initial is not None:
            self.plot.axes.legend()

        self.plot.draw()

    def draw(self):
        """Initial drawing of the plot."""
        self.plot.axes.imshow(self.image, cmap=plt.get_cmap("binary_r"))
        self.plot.axes.set_title(
            "Left click to add a control node.\n"
            "At least 3 are needed to perform a segmentation."
        )
        self.plot.draw()

    def perform_segmentation(self):
        """Gets all the parameters from the widgets and performs the segmentation."""
        sigma = self.controls.gauss_width
        resolution = self.controls.resolution
        degree = self.controls.degree

        segment, initial = segment_one_image(
            self.image, self.nodes, sigma=sigma, resolution=resolution, degree=degree
        )

        self.controls.reset_button.setEnabled(True)
        self.controls.segment_button.setEnabled(False)

        self.nodes = []
        self.redraw(segment, initial)

    def read_image(self, *args):
        """Opens the image to segment."""
        self.image = imread(INSECTS, as_gray=True)
        self.draw()
        self.plot.canvas.mpl_connect("button_release_event", self.add_node)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    gui = MySimpleGUI()
    gui.show()

    sys.exit(app.exec_())
