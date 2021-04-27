# GUIs for Python - improving the accessibility of research software 
 
Research software has been a driving force behind the birth and rapid growth of informatics, but it was the appearance of graphical user interfaces (GUIs) in the 1980s that made computers accessible to everyone. A GUI helps to reduce the learning curve for using software, increases the base of potential users and can ultimately increase citations and impact. Moreover, a well-designed GUI can perform validation and increase the robustness and reproducibility of the results, productively decoupling developers from users. 
 
This repository contains simple examples on using three GUI frameworks (Jupyter Widgets, Kivy and Tkinter) to perform the same tasks. A handy [cheatsheet](python_guis/cheatsheet.md) has been created providing quick access to a range of information for the three frameworks. 

## Installation instructions for a fresh Ubuntu Desktop 18.04 system

These instructions have been tested with Lubuntu but should be valid for other ubuntu-based desktop Linux distributions:

```bash
sudo apt update
sudo apt install git python3-venv python3-tk
git clone https://github.com/ImperialCollegeLondon/python-guis.git
cd python-guis
python3 -mvenv venv
. venv/bin/activate
pip install -U setuptools wheel pip
pip install -e .
garden install matplotlib --kivy
```

## Installation instructions for macOS:

Tested on Mojave (10.14) using Python 3.7 installed directly from Python.org. Python installed with `homebrew` or `macports` should also work, but there is a [known issue](https://github.com/matplotlib/matplotlib/issues/9637#issuecomment-515081488) when scrolling on a Matplotlib figure embedded in Tkinter that causes it to crash. Anaconda Python should also work although it is untested:

```bash
git clone https://github.com/ImperialCollegeLondon/python-guis.git
cd python-guis
python3 -mvenv venv
. venv/bin/activate
pip install -U setuptools wheel pip
pip install -e .
garden install matplotlib --kivy
```

## Installation instructions for Windows 10:

The following installation instructions have been tested on Windows 10 using Git Bash ([some extra configuration](https://stackoverflow.com/a/56170202/3778792) may be required) and PowerShell (you may temporarily need to disable the security directives in order to activate the virtual environment) with Anaconda Python 3.7.

```bash
git clone https://github.com/ImperialCollegeLondon/python-guis.git
cd python-guis
python -mvenv venv
. venv/Scripts/activate
pip install -U setuptools wheel pip
pip install docutils pygments pypiwin32 kivy_deps.sdl2 kivy_deps.glew
pip install -e .
garden install matplotlib --kivy
```

On Windows 10, there are known, system specific, issues that may prevent Kivy from working as expected. You may receive an error about having an old version of OpenGL or just see a black window with no widgets. If you encounter one of these issues, try one of the solutions suggested [here](https://stackoverflow.com/questions/52109670/cannot-display-anything-but-a-solid-color-window-with-kivy).
