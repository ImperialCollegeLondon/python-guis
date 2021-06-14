# Examples

## A minimum working example (MWE)

The MWE for the three frameworks will have the following elements:

- A button saying "Click me!"
- A non-editable text area showing a text after clicking the button.
- A top container/main window holding the above two side by side.

We will ignore anything related to aesthetics or customisation of the look and feel, although that is often a big part of the creation of the GUI. The reason is that the three frameworks differ massively in how to do this, so it is best to focus on how to achieve the same functionality, for now. 

### **Jupyter Widgets** (Needs to be run within a Jupyter notebook)

```python
import ipywidgets as widgets
from IPython.display import display

def on_button_clicked(button):
    label.value = "Hello Pythoners!"

# Create the widgets.
button = widgets.Button(description="Click me")
label = widgets.Label(value='')
hbox = widgets.HBox()

# Add them to a container. This includes setting their physical arrangement. 
hbox.children=[button, label]

# Add the callback of the button.
button.on_click(on_button_clicked)

# Display the top container.
display(hbox)
```

### **Tkinter**

- [The obligatory first program](https://tkdocs.com/tutorial/install.html#helloworld)
    
```python
import tkinter as tk
from tkinter import ttk

def on_button_clicked():
    label["text"] = "Hello Pythoners!"

# Create the widgets. This includes adding them to a container.
root = tk.Tk()
button = ttk.Button(master=root, text="Click me")
label = ttk.Label(master=root, text="")

# Create their physical arrangement.
button.pack(side=tk.LEFT)
label.pack(side=tk.LEFT)

# Add the callback of the button.
button.configure(command=on_button_clicked)

# Run the main window loop, which starts the program.
root.mainloop()
```

When manipulating the content of other widgets, Tkinter often uses special variables that can retrieve or set those values and update the whole GUI in the process. For example, `tk.StringVar` can be used to set or get string variables. Others are `tk.DoubleVar`, `tk.IntVar` and `tk.BoolVar`. Applied to the previous example, we could write:

```python
label_var = tk.StringVar()
label = ttk.Label(master=root, textvariable=label_var)
```

And then change the `on_button_clicked` to:

```python
def on_button_clicked():
    label_var.set("Hello Pythoners!")
```

### **Kivy**

- [Creating a basic Kivy application](https://kivy.org/doc/stable/guide/basic.html#create-an-application)
    
```python
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

def on_button_clicked(label):
    label.text = "Hello Pythoners!"
    
# Create main application.
class HelloApp(App):
    def build(self):
        
        # Create the widgets.
        hbox = BoxLayout()
        button = Button(text="Click me")
        label = Label(text="")
        
        # Add them to a container. This includes setting their physical arrangement. 
        hbox.add_widget(button)
        hbox.add_widget(label)
        
        # Add the callback of the button.
        button.bind(on_press=lambda button: on_button_clicked(label))
        
        # Return the top container. This can be any widget
        return hbox

# Run the main windoow loop, which starts the program.
if __name__ == "__main__":
    
    from kivy.config import Config
    # We don't want a fullscreen App here.
    Config.set("graphics", "fullscreen", "0")

    HelloApp().run()
```

Kivy has an alternative method for defining the interface, separating the definition of the widgets and all its properties from the logic. In this case, the widgets are defined in a ".kv" file which is used to build the interface automatically when loading. The examples `mwe_kivy_with_kv.py` and `hello.kv` result in the same application that the previous example but separating the interface definition and the logic. The Kivy documentation has more information on the [Kv language](https://kivy.org/doc/stable/guide/lang.html).

Note: Running Tkinter or Kivy within a Jupyter notebook might cause the kernel to fail on exit. Better to run them as normal Python scripts.

## Plotting

### **Jupyter Widgets**

The creation of the figure and data plotting has to be done within an [Output widget](https://ipywidgets.readthedocs.io/en/stable/examples/Output%20Widget.html) context manager. Indeed, output widgets can be used to display pretty much anything, from standard output, to errors, videos, figures, etc. The Output widget has to be arranged within a container as with any other widget.

If the plot is to be interactive, then the directive `%matplotlib notebook` has to be used before importing Matplotlib. Otherwise, `%matplotlib inline` is enough, displaying the figure as an image.

The following example displays a label and a plot side by side. We connect an event to the figure canvas to draw points when we click on the plot.

```python
%matplotlib notebook
import ipywidgets as widgets
from IPython.display import display

import matplotlib.pyplot as plt
import numpy as np


def on_canvas_click(event):
    if event.inaxes:
        event.inaxes.plot([event.xdata], [event.ydata], marker="o", color="r")
        event.canvas.draw()


data = np.random.random((10, 10))

# Create the widgets and display the top container.
label = widgets.Label(value="Click on the plot as many times as you want!")
out1 = widgets.Output()
hbox = widgets.HBox(children=[label, out1])
display(hbox)

# Define what should be shown in the Output widget
with out1:
    fig, axes = plt.subplots()
    axes.imshow(data)
    fig.canvas.mpl_connect("button_press_event", on_canvas_click)
    fig.canvas.draw()
```

### **Tkinter**

Matplotlib has builtin support for Tkinter, providing a backend that replaces the default figure canvas by a Tkinter canvas. The Tkinter version of the navigation toolbar can also be added to the GUI.

The following example is the Tkinter version of the above:

```python
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
```

### **Kivy**

Kivy works very similar to Tkinter, but in this case the backend is provided as part of the community-contributed Kivy Garden packages, as discussed [above](#installation). You will notice that this backend has built-in the capability of drawing (and dragging) red points on the plot. Try using the right click!

The interactive plot example using Kivy will look like this:

```python
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

```
