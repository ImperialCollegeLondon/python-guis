from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout

Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "600")


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

    def on_segment(self):
        from numpy import array
        from skimage.io import imread

        controls = self.ids.control_field
        display = self.ids.play_field
        degree = int(controls.degree)
        resolution = int(controls.resolution)
        width = int(controls.ids.gaussian_width.value)

        image = imread(self.ids.play_field.image, as_gray=True)
        factor = array(image.shape) / array(display.ids.image.size)
        offset = array(display.ids.image.pos) - array(display.pos)
        points = array(self.control_points) * factor + offset

        segment(points, image, degree=degree, resolution=resolution, width=width)


def segment(points, image, degree=2, resolution=360, width=2):
    pass


class BeetleApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    BeetleApp().run()
