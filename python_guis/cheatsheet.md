# Cheatsheet for Jupyter Widgets, Tkinter and Kivy

This document shows the (rough) equivalence between the main widgets in the three GUI frameworks. While the functionality is somewhat similar, their inputs and how they are used or packed together might differ substantially.

This is by no means an exhaustive lists of widgets (in particular for Kivy, which has an extensive list of specialised widgets) but just a few common ones that work in a similar way in the three frameworks. 

The main sources of information and reference for each of the frameworks are:

- *Jupyter Widgets*:

    - [Official Jupyter Widgets documentation](https://ipywidgets.readthedocs.io/en/stable/index.html)

- *Tkinter*:

    -   [Official Python documentation on Tk themed widgets](https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Notebook)
    -   [TkDocs](https://tkdocs.com/tutorial/index.html)
    -   [Effbot](https://effbot.org/tkinterbook/): Largely outdated, but still useful for some things related to the basic `tk` widgets (see below). 
    
- *Kivy*:

    - [Official Guides](https://ipywidgets.readthedocs.io/en/stable/index.html)
    - [API Reference](https://kivy.org/doc/stable/api-kivy.html)
    - [Wiki](https://github.com/kivy/kivy/wiki)

## Installation

- *Matplotlib*:

Plots are common elements in most research software. None of the above frameworks have any widget related to plots, but all of them have support to incorporating figures created with Matploltib,  the most common (although not the only one) plotting library in Python. Matplotlib can be installed with:

```bash
pip install matplotlib
```

- *Jupyter Widgets*:

Jupyter Widgets requires Jupyter, of course, and the `ipywidgets` package, and to enable the widget extension in Jupyter. Assuming you've already [installed Jupyter](https://jupyter.readthedocs.io/en/latest/install.html), [installing the widgets](https://ipywidgets.readthedocs.io/en/stable/user_install.html) should be straightforward either with pip or conda:

```bash
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension
```

or 

```bash
conda install -c conda-forge ipywidgets
```

The conda command automatically enables the extension. Depending on your system, installing Jupyter might install and enable the widgets automatically.

- *Tkinter*:

[Tkinter is part of the standard Python library](https://docs.python.org/3/library/tk.html) so chances are that nothing else needs to be done in order to use it. However, in some Linux distributions it is provided as a separate package. For example, in Ubuntu you will need to run:

```bash
sudo apt install python3-tk
```

- *Kivy*:

Kivy webpage offers [very detailed instructions](https://kivy.org/#download) for its installation on the main OS. There are precompiled wheels that can be installed using pip, in addition to optional dependencies:

```bash
pip install kivy
```

Kivy can also be installed using conda with:

```bash
conda install kivy -c conda-forge
```

Extra tools are needed in order to run Kivy examples in Android or IOS. 

Many addons are distributed as part of [Kivy Garden](https://kivy-garden.github.io), developed and mantained by the community. One of them is the Kivy backend for Matplotlib, which we will use below. 

There are different instructions depending on the *vintage* of the *flower*, as Kivy Garden addons are called. In particular, to install the Matplotlib backend, first install the [legacy kivy-garden](https://kivy.org/doc/stable/api-kivy.garden.html#legacy-garden-tool-instructions) tool with pip and then use that tool to install the backend:

```bash
pip install kivy-garden
garden install matplotlib
```

## Pre-requisites

The following import statements need to be called before importing the widgets below:

- *Jupyter Widgets*:

```python
import ipywidgets as widgets
```

- *Tkinter*:

```python
from tkinter import ttk
```

and for some older widgets:

```python
import tkinter as tk
```
    
- *Kivy*:

Each widget lives in its own submodule of `uix`:

```python
from kivy import uix
```

## Common widgets

|  | *Jupyter* | *Tkinter* | *Kivy* |
|--------|---------|---------|------|
| *Button* | [`widgets.Button(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Button)| [`ttk.Button(...)`](https://tkdocs.com/tutorial/widgets.html#button) | [`uix.button.Button(...)`](https://kivy.org/doc/stable/api-kivy.uix.button.html?highlight=button#module-kivy.uix.button)|
| *Label* | [`widgets.Label(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Label)| [`ttk.Label(...)`](https://tkdocs.com/tutorial/widgets.html#label) | [`uix.label.Label(...)`](https://kivy.org/doc/stable/api-kivy.uix.label.html?highlight=label#module-kivy.uix.label)|
| *Entry*<br>(1-line) | [`widgets.Text(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Text)| [`ttk.Entry(...)`](https://tkdocs.com/tutorial/widgets.html#entry)| [`uix.textinput.Textinput(..., multiline=False)`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html?highlight=textinput#module-kivy.uix.textinput)|
| *Text*<br>(multi-line) | [`widgets.Textarea(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Textarea)| [`tk.Text(...)`](https://tkdocs.com/tutorial/morewidgets.html#text) | [`uix.textinput.Textinput(...)`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html?highlight=textinput#module-kivy.uix.textinput)|
| *Radio buttons* | [`widgets.RadioButtons(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#RadioButtons)| [`ttk.Radiobutton(..., variable=…)`](https://tkdocs.com/tutorial/widgets.html#radiobutton) | [`uix.checkbox.CheckBox(..., group=…)`](https://kivy.org/doc/stable/api-kivy.uix.checkbox.html?highlight=checkbox#module-kivy.uix.checkbox)|
| *Checkbox* | [`widgets.RadioButtons(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Checkbox)| [`ttk.Checkbutton(...)`](https://tkdocs.com/tutorial/widgets.html#checkbutton) |[`uix.checkbox.CheckBox(...)`](https://kivy.org/doc/stable/api-kivy.uix.checkbox.html?highlight=checkbox#module-kivy.uix.checkbox)|
| *Dropdown* | [`widgets.Dropdown(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Dropdown)| [`ttk.Combobox(...)`](https://docs.python.org/3/library/tkinter.ttk.html#combobox) | [`uix.spinner.Spinner(...)`](https://kivy.org/doc/stable/api-kivy.uix.spinner.html?highlight=spinner#module-kivy.uix.spinner)|
| *Slider* | [`widgets.IntSlider(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#IntSlider)<br>[`widgets.FloatSlider(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#FloatSlider)| [`tk.Scale(...)`](https://tkdocs.com/tutorial/morewidgets.html#scale) | [`uix.slider.Slider(...)`](https://kivy.org/doc/stable/api-kivy.uix.slider.html?highlight=slider#module-kivy.uix.slider)|

## Container and layout widgets

The above widgets do not exist on their own: they all need to be placed within a container (can be the top window of the application) and arranged in a certain way within the container. This task is performed by container/layout widgets. 

### *Jupyter Widgets* and *Kivy* work in a similar way:

The basic containers are vertical and horizontal boxes that can host several widgets in a row ([HBox](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#HBox) and [VBox](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#VBox) for Jupyer and [BoxLayout](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#module-kivy.uix.boxlayout) or [GridLayout](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#module-kivy.uix.gridlayout) for Kivy). The way of using them is:

1. All the relevant widgets (buttons, labels, etc.) are first created. Nothing in their creation has anything to do with where they will be placed. 
2. The widgets are added to a container (including all other containers except for the top one), often with some information about their size, alignment, padding, if they should resize with the container, etc.
3. The position of the children within the container is automatic in the order they are added. To have a more or less accurate position of the widgets, a combination of horizontal, vertical and grid containers have to be used.[3](#kivi-layouts)
4. The last, top level container does not need to be added to another container as it is assumed it fills the entire App window (Kivy) or output cell (Jupyter Widgets).

**Example:** The labels are placed next to each other left to right, with 0 on the left and 3 on the right. Note that `hbox` also has to be added to a container, unless it is the top container.

```python
# Jupyter Widgets
hbox = widgets.HBox()
hbox.children = [widgets.Label(str(i)) for i in range(4)]

# Kivy
hbox = uix.boxlayout.BoxLayout()
for i in range(4):
    hbox.add_widget(uix.label.Label(text=str(i)))
```

<a name="kivi-layouts">3</a>: Note that Kivy has a [large variety of specialised layouts](https://kivy.org/doc/stable/api-kivy.uix.layout.html) that do not follow the above description and that, ultimately, allow the user to put the widgets wherever they want using relative or absolute coordinates.

### *Tkinter* follows a different approach:

In Tkinter, how things are arranged do not depend on the container (which will be `ttk.Frame` most of the times) but on the geometry manager used. The process in this case will be:

1. During creation, all widgets are assigned a parent, meaning that the parent must exists when the widget is created.
2. The widgets are placed somewhere within the parent, often with some information about their alignment, padding, etc. using a geometry manager [4](#tkinter-layouts): 
    - The [`Pack` geometry manager](https://effbot.org/tkinterbook/pack.htm) works like *Jupyter Widgets* and *Kivy* containers, arranging widgets automatically in the order they are being packed, either vertically or horizontally.
    - The [`Grid` geometry manager](https://tkdocs.com/tutorial/grid.html) allows to specify exact row and column for the children widgets, how many of these they should span as well as how they should resize with the container.
4. The top container must be the `tk.Tk` main window, from which all children hang. 

**Example:** For the `Pack` manager, the labels are placed next to each other left to right, with 0 on the left and 3 on the right. For the `Grid` manager, a specific row and column is chosen, in this case filling a diagonal. Note that `hbox` also has to be packed or grid in order to have it visible. 

```python
# Using Pack
hbox = ttk.Frame(master=parent_container)
for i in range(4):
    ttk.Label(master=hbox, text=str(i)).pack(side=tk.LEFT)

# Using Grid
hbox = ttk.Frame(master=parent_container)
for i in range(4):
    ttk.Label(master=hbox, text=str(i)).grid(column=i, row=i)
```

<a name="tkinter-layouts">4</a>: Like the specialised Kivy layouts, Tkinter also has the [`Place` geometry manager](https://effbot.org/tkinterbook/place.htm) that allows to place the widgets virtually anywhere in absolute or relative terms. 

### Notebook and PageLayout

Notebook ([Jupyter Widgets](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Tabs) and [Tkinter](https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Notebook)) and PageLayout ([Kivy](https://kivy.org/doc/stable/api-kivy.uix.pagelayout.html#module-kivy.uix.pagelayout)) are both used to create a tab-based or multi-page layout, with the possibility of changing to one another by clicking on the tab/page border. 

In both cases, it is recommended - although not necessary - that each of the tabs/pages to be a container/layout widget itself as those shown above with as many children widgets as needed. 

Jupyter Widgets notebook with 3 tabs:
```python
hbox1 = widgets.HBox()
hbox2 = widgets.HBox()
hbox3 = widgets.HBox()

book = widgets.Tab()
book.children = [hbox1, hbox2, hbox3]
```

Tkinter notebook with 3 tabs:
```python
book = ttk.Notebook(master=parent_container)

hbox1 = ttk.Frame(master=book)
hbox2 = ttk.Frame(master=book)
hbox3 = ttk.Frame(master=book)

book.add(hbox1)
book.add(hbox2)
book.add(hbox3)
```

Kivy PageLayout with 3 pages:
```python
hbox1 = uix.boxlayout.BoxLayout()
hbox2 = uix.boxlayout.BoxLayout()
hbox3 = uix.boxlayout.BoxLayout()

book = uix.pagelayout.PageLayout()

book.add_widget(hbox1)
book.add_widget(hbox2)
book.add_widget(hbox3)
```

## A minimum working example (MWE)

The MWE for the three frameworks will have the following elements:

- A button saying "Click me!"
- A non-editable text area showing a text after clicking the button.
- A top container/main window holding the above two side by side.

We will ignore anything related to aesthetics or customisation of the look and feel, although that is often a big part of the creation of the GUI. The reason is that the three frameworks differ massively in how to do this, so it is best to focus on how to achieve the same functionality, for now. 

- **Jupyter Widgets** (Needs to be run within a Jupyter notebook)
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

- **Tkinter**

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

- **Kivy**

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

- **Jupyter Widgets**

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

- **Tkinter**

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

- **Kivy**

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