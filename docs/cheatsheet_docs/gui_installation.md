# Installation of the frameworks

**Note:** If you followed the [installation instructions for this repository](../installation.md), you already have all you need in the virtual environment. This guide refers of what you will need to install if you want to use the frameworks in your own software.

## *Matplotlib*:

Plots are common elements in most research software. None of these frameworks have any widget related to plots, but all of them have support to incorporating figures created with Matploltib,  the most common (although not the only one) plotting library in Python. Matplotlib can be installed with:

```bash
pip install matplotlib
```

## *Jupyter Widgets*:

Jupyter Widgets requires Jupyter, of course, and the `ipywidgets` package, and to enable the widget extension in Jupyter. Assuming you've already [installed Jupyter](https://jupyter.readthedocs.io/en/latest/install.html), [installing the widgets](https://ipywidgets.readthedocs.io/en/stable/user_install.html) should be straightforward either with pip or conda:

```bash
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension
```

or 

```bash
conda install -c conda-forge ipywidgets
```

The conda command automatically enables the extension. **Depending on your system, installing Jupyter might install and enable the widgets automatically.**

## *Tkinter*:

[Tkinter is part of the standard Python library](https://docs.python.org/3/library/tk.html) so chances are that nothing else needs to be done in order to use it. However, in some Linux distributions it is provided as a separate package. For example, in Ubuntu you will need to run:

```bash
sudo apt install python3-tk
```

## *Kivy*:

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