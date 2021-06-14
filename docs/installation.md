# Installation

These installation instructions will install the contents of this repository as long as all its dependencies within a virtual environment in your system. The installation will be done in "edit mode" to allow you to make changes to any of the files, play around with the gui examples and letting you learn by trying out things. 

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

Tested on Mojave (10.14) using Python 3.7 and 3.8 installed directly from Python.org. Python installed with `homebrew` or `macports` should also work, but there is a [known issue](https://github.com/matplotlib/matplotlib/issues/9637#issuecomment-515081488) when scrolling on a Matplotlib figure embedded in Tkinter that causes it to crash. Anaconda Python should also work although it is untested:

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
