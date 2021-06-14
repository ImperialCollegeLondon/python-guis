from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from matplotlib.pyplot import Figure
import numpy as np

Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "600")


class Matplotlib(FigureCanvasKivyAgg):
    control_points = ListProperty([])
    contour = ObjectProperty(None, allownone=True, force_dispatch=True)
    initial = ObjectProperty(None, allownone=True, force_dispatch=True)
    controls = ObjectProperty(None)
    diameter = 30.0

    def __init__(self, **kwargs):
        from skimage.io import imread
        from python_guis import INSECTS

        self.figure = Figure(tight_layout=True)

        super().__init__(self.figure, **kwargs)
        self.figure.patch.set_visible(False)
        self.image_data = imread(INSECTS, as_gray=True)

        def add_control_point(event):
            if self.contour is not None:
                self.remove_all()

            if event.inaxes is not None:
                self.control_points.append((event.xdata, event.ydata))

        self.bind(
            control_points=lambda *args: self.draw(), contour=lambda *args: self.draw()
        )
        self.mpl_connect("button_release_event", add_control_point)

    def draw(self):
        from matplotlib import pyplot as plt

        self.figure.clear()
        axes = self.figure.add_subplot()
        axes.imshow(self.image_data, cmap=plt.get_cmap("binary_r"))
        axes.set_title(
            "Left click to add a control node.\n"
            "At least 3 are needed to perform a segmentation."
        )
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        self.draw_control_points(axes)
        self.draw_contour(axes)
        return super().draw()

    def remove_all(self):
        """Removes all control points and segments."""
        self.initial = None
        self.contour = None
        self.control_points = []

    def draw_control_points(self, axes):
        if len(self.control_points) == 0:
            return

        xy = np.array(self.control_points + [self.control_points[0]])
        axes.plot(*xy.T, "ro-")

    def draw_contour(self, axes):
        if self.contour is None:
            return

        axes.plot(*self.initial.T, color="blue", label="Initial")
        axes.plot(*self.contour.T, color="orange", label="Segmented")

    def on_segment(self, degree, resolution, sigma):
        from python_guis.model import segment_one_image
        from kivy.clock import Clock

        degree = int(degree)
        resolution = int(getattr(resolution, "text", resolution))
        sigma = int(getattr(sigma, "value", sigma))

        self.controls.disabled = True
        self.disabled = True

        def reenable(*args):
            """Enables controls.

            In order to ensure that clicks which happen during the computation are not
            taken into account, we have to make sure the fields are disabled while these
            clicks are processed. That means the computation will schedule un-disabling
            for the frame after it is itself completed.
            """
            self.controls.disabled = False
            self.disabled = False

        def computation(*args):
            """Performs contour computations.

            Computations are started in the next frame, *after* disabling the fields
            becomes visible.

            Note: async/await has landed in kivy dev. Eventually, computations should be
            performed asynchronously, rather than through a chain of calls to
            schedule_once.
            """
            contour, initial = segment_one_image(
                nodes=self.control_points,
                image=self.image_data,
                degree=degree,
                resolution=resolution,
                sigma=sigma,
            )
            self.initial = initial
            self.contour = contour
            Clock.schedule_once(reenable, 0)

        Clock.schedule_once(computation, 0)


class Controls(StackLayout):
    degree = NumericProperty(1)

    def on_resolution_change(self, textinput):
        try:
            int(textinput.text)
        except ValueError:
            textinput.text = str(self.resolution)


class MainWindow(BoxLayout):
    pass


class BeetleApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    from python_guis.kivy.gui_kivy import BeetleApp  # noqa

    BeetleApp().run()
