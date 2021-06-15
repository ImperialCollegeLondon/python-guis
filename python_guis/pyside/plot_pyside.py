import sys

if sys.platform == "darwin":
    # There is an issue with pyside2 and MacOS BigSur. This hack sorts it
    # https://stackoverflow.com/a/64878899/3778792
    import os

    os.environ["QT_MAC_WANTS_LAYER"] = "1"

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide2 import QtWidgets


def on_canvas_click(event):
    if event.inaxes:
        event.inaxes.plot([event.xdata], [event.ydata], marker="o", color="r")
        event.canvas.draw()


class MySimpleGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Click on the plot as many times as you want!")

        # Create the figure.
        data = np.random.random((10, 10))
        fig = Figure()
        self.axes = fig.add_subplot()
        self.axes.imshow(data)
        self.canvas = FigureCanvasQTAgg(fig)

        plot_area = QtWidgets.QWidget()
        plot_area.setLayout(QtWidgets.QVBoxLayout())
        toolbar = NavigationToolbar2QT(self.canvas, plot_area)
        plot_area.layout().addWidget(self.canvas)
        plot_area.layout().addWidget(toolbar)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(plot_area)

        self.canvas.mpl_connect("button_press_event", on_canvas_click)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    gui = MySimpleGUI()
    gui.show()

    sys.exit(app.exec_())
