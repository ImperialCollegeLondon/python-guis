import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np


def on_canvas_click(event):
    if event.inaxes:
        event.inaxes.plot([event.xdata], [event.ydata], marker="o", color="r")
        event.canvas.draw()


data = np.random.random((10, 10))

# Create the widgets.
root = tk.Tk()
ttk.Label(root, text="Click on the plot as many times as you want!").pack(side=tk.LEFT)

# Create the figure.
fig = Figure()
axes = fig.add_subplot()
axes.imshow(data)

# And use the Tkinter version of the canvas and the toolbar.
# Both need to be packed (or grid) as with any other widget.
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT)
canvas.mpl_connect("button_press_event", on_canvas_click)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack(side=tk.TOP)
toolbar.update()

# Run the main window loop, which starts the program.
root.mainloop()
