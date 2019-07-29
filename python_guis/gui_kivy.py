from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from matplotlib.pyplot import Figure

Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "600")


class Matplotlib(FigureCanvasKivyAgg):
    image = StringProperty(str(Path(__file__).parent / "insects.jpg"))
    control_points = ListProperty([])
    node_points = ListProperty([])
    diameter = 30.0

    def __init__(self, **kwargs):
        from skimage.io import imread

        self.figure = Figure(tight_layout=True)

        super().__init__(self.figure, **kwargs)
        self.figure.patch.set_visible(False)
        self.figure.canvas.mpl_connect("button_release_event", self.add_node)
        self.image_data = imread(str(self.image), as_gray=True)

    def draw(self):
        from matplotlib import pyplot as plt

        self.figure.clear()
        axes = self.figure.add_subplot()
        axes.imshow(
            self.image_data, cmap=plt.get_cmap("binary_r")
        )
        axes.set_title(
            "Left click to add a control node.\n"
            "At least 3 are needed to perform a segmentation."
        )
        axes.axis("off")
        self.draw_control_points(axes)
        return super().draw()

    def add_node(self, event):
        if event.inaxes is None:
            return
        self.control_points.append((event.xdata, event.ydata))
        self.draw_control_points(event.inaxes)
        self.figure.canvas.draw()

    def draw_control_points(self, axes):
        if len(self.control_points) == 0:
            return

        x, y = (
            [x[0] for x in self.control_points] + [self.control_points[0][0]],
            [x[1] for x in self.control_points] + [self.control_points[0][1]],
        )
        axes.plot(x, y, "ro-")


class ControlField(StackLayout):
    degree = NumericProperty(1)
    resolution = NumericProperty(360)

    def on_resolution_change(self, textinput):
        try:
            self.resolution = int(textinput.text)
        except ValueError:
            textinput.text = str(self.resolution)


class PlayField(FloatLayout):
    image = StringProperty(str(Path(__file__).parent / "insects.jpg"))
    diameter = 30.0

    def on_touch_down(self, touch):
        if touch.button != "left" or not self.collide_point(*touch.pos):
            return False
        if super().on_touch_down(touch):
            return True
        touch.grab(self)
        self.parent.control_points.append(touch.pos)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.parent.control_points[-1] = touch.pos
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super().on_touch_up(touch)


class MainWindow(BoxLayout):
    control_points = ListProperty([])
    node_points = ListProperty([])

    def on_segment(self):
        from numpy import array
        from skimage.io import imread
        from .model import segment_one_image

        controls = self.ids.control_field
        display = self.ids.play_field
        degree = int(controls.degree)
        resolution = int(controls.resolution)
        sigma = int(controls.ids.gaussian_width.value)

        image = imread(self.ids.play_field.image, as_gray=True)
        factor = array(
            [
                image.shape[1] / display.ids.image.width,
                image.shape[0] / display.ids.image.height,
            ]
        )
        points = (array(self.control_points) - array(display.ids.image.pos)) * factor

        contour, initial = segment_one_image(
            nodes=points, image=image, degree=degree, resolution=resolution, sigma=sigma
        )
        contour = contour / factor + display.ids.image.pos
        initial = initial / factor + display.ids.image.pos
        self.node_points = [
            (contour[i, 0], contour[i, 1]) for i in range(contour.shape[0])
        ]


class BeetleApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    from python_guis.gui_kivy import BeetleApp  # noqa

    BeetleApp().run()
