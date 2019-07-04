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


## Pre-requisites

The following import statements need to be called before importing the widgets below:

| *Jupyter* | *Tkinter* | *Kivy* |
|:---------:|:---------:|:------:|
| `import ipywidgets as widgets`  | `from tkinter import ttk`<br>or for some widgets:<br>`import tkinter as tk`| Each widget lives in its own submodule of:<br>`from kivy import uix`|

## Common widgets

|  | *Jupyter* | *Tkinter* | *Kivy* |
|--------|---------|---------|------|
| *Button* | [`widgets.Button(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Button)| [`ttk.Button(...)`](https://tkdocs.com/tutorial/widgets.html#button) | [`uix.button.Button(...)`](https://kivy.org/doc/stable/api-kivy.uix.button.html?highlight=button#module-kivy.uix.button)|
| *Label* | [`widgets.Label(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Label)| [`ttk.Label(...)`](https://tkdocs.com/tutorial/widgets.html#label) | [`uix.label.Label(...)`](https://kivy.org/doc/stable/api-kivy.uix.label.html?highlight=label#module-kivy.uix.label)|
| *Entry*<br>(1-line) | [`widgets.Text(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Text)| [`ttk.Entry(...)`](https://tkdocs.com/tutorial/widgets.html#entry)| [`uix.textinput.Textinput(...)`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html?highlight=textinput#module-kivy.uix.textinput)[1](#multiline)|
| *Text*<br>(multi-line) | [`widgets.Textarea(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Textarea)| [`tk.Text(...)`](https://tkdocs.com/tutorial/morewidgets.html#text) | [`uix.textinput.Textinput(...)`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html?highlight=textinput#module-kivy.uix.textinput)|
| *Radio buttons* | [`widgets.RadioButtons(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#RadioButtons)| [`ttk.Radiobutton(...)`](https://tkdocs.com/tutorial/widgets.html#radiobutton)[2](#groups) | [`uix.checkbox.CheckBox(...)`](https://kivy.org/doc/stable/api-kivy.uix.checkbox.html?highlight=checkbox#module-kivy.uix.checkbox)[2](#groups)|
| *Checkbox* | [`widgets.RadioButtons(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Checkbox)| [`ttk.Checkbutton(...)`](https://tkdocs.com/tutorial/widgets.html#checkbutton) |[`uix.checkbox.CheckBox(...)`](https://kivy.org/doc/stable/api-kivy.uix.checkbox.html?highlight=checkbox#module-kivy.uix.checkbox)|
| *Dropdown* | [`widgets.Dropdown(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Dropdown)| [`ttk.Combobox(...)`](https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Combobox) | [`uix.spinner.Spinner(...)`](https://kivy.org/doc/stable/api-kivy.uix.spinner.html?highlight=spinner#module-kivy.uix.spinner)|
| *Slider* | [`widgets.IntSlider(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#IntSlider)<br>[`widgets.FloatSlider(...)`](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#FloatSlider)| [`tk.Scale(...)`](https://tkdocs.com/tutorial/morewidgets.html#scale) | [`uix.slider.Slider(...)`](https://kivy.org/doc/stable/api-kivy.uix.slider.html?highlight=slider#module-kivy.uix.slider)|

<a name="multiline">1</a>: Set argument `multiline=False`. 

<a name="groups">2</a>: There has to be one of this statements per button, all linked to the same `variable` (Tkinter) or the same `group` (Kivy). 


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