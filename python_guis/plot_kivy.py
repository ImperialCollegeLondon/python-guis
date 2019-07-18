from kivy.garden.matplotlib.backend_kivyagg import (
    FigureCanvasKivyAgg,
    NavigationToolbar2Kivy,
)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from matplotlib.figure import Figure
import numpy as np


def on_canvas_click(event):
    if event.inaxes:
        event.inaxes.plot([event.xdata], [event.ydata], marker="o", color="r")
        event.canvas.draw()


# Create main application.
class HelloApp(App):
    def build(self):
        data = np.random.random((10, 10))

        # Create the widgets. We need a vertical box to arrange the navigation toolbar
        hbox = BoxLayout()
        vbox = BoxLayout(orientation="vertical")
        label = Label(text="Click on the plot as many times as you want!")

        # Create the figure.
        fig = Figure()
        axes = fig.add_subplot()
        axes.imshow(data)
        canvas = FigureCanvasKivyAgg(fig)
        nav = NavigationToolbar2Kivy(canvas)

        # Add them to a container.
        vbox.add_widget(canvas)
        vbox.add_widget(nav.actionbar)
        hbox.add_widget(label)
        hbox.add_widget(vbox)

        # Add the callback of the canvas.
        canvas.mpl_connect("button_press_event", on_canvas_click)
        canvas.draw()

        # Return the top container. This can be any widget
        return hbox


# Run the main windoow loop, which starts the program.
if __name__ == "__main__":
    from kivy.config import Config

    # We don't want a fullscreen App here.
    Config.set("graphics", "fullscreen", "0")

    HelloApp().run()
