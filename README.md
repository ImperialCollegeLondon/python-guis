# GUIs for Python - improving the accessibility of scientific software 
 
Research software has been a driving force behind the birth and rapid growth of informatics, but it was the appearance of graphic user interfaces (GUI) in the 1980s that made computers accessible to everyone. A GUI helps to reduce the learning curve for using software, increases the base of potential users and can ultimately increase citations and impact. Moreover, a well-designed GUI can perform validation and increase the robustness and reproducibility of the results, productively decoupling developers from users. 
 
This workshop will have three parts. In the first one, we will give an introduction to GUIs and review three of the most common Python packages to create them: Tkinter for the desktop, Jupyter Widgets for web and Kivy for mobile devices (45 min). The second part will be a hands-on session where attendees will explore a complete GUI done with the framework of their choice and go through a range of exercises to learn the basics of GUI development (90 min). The last part will provide guidance on how to plan and implement a GUI, considering the target users, their objectives, accessibility, providing contextual help, etc. Finally, organized in groups and keeping this user-centric concepts of GUI development fresh, the attendees will design a GUI of a well known command line software: Git (45 min). 


# Installation instructions

A virtual machine (VM) will be accessible with all the Python packages, libraries and examples required by the workshop pre-installed. However, if you prefer to setup your own laptop for the workshop, please follow the instructions below. 

## Using the Workshop Virtual Machine

 Connection details will be provided when entering into the workshop. To access the VM you will need a Remote Desktop Client:

- Windows: It should include Remote Desktop already
- MacOS: [Microsoft Remote Desktop](https://apps.apple.com/gb/app/microsoft-remote-desktop-10/id1295203466?mt=12) is available in the App Store (free)
- Linux: Tested using [Remmina](https://remmina.org). It comes with Ubuntu and should be available in most Linux distributions. 

## Installation instructions on a fresh Ubuntu Desktop 18.04 system

Tested with Lubuntu, but these are probably valid in any other ubuntu-based desktop environment:

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

## Installation instructions on macOS:

Tested on Mojave (10.14) using Python 3.7 installed directly from Python.org. Python installed with `homebrew` should also work, but there is a [known issue](https://github.com/matplotlib/matplotlib/issues/9637#issuecomment-515081488) when scrolling on a Matplotlib figure embedded in Tkinter that causes it to crash. Anaconda Python should also work - not tested, thought.

```bash
git clone https://github.com/ImperialCollegeLondon/python-guis.git
cd python-guis
python3 -mvenv venv
. venv/bin/activate
pip install -U setuptools wheel pip
pip install -e .
garden install matplotlib --kivy
```

## Installation instructions on Windows 10:

The following installation instructions have been tested in Windows 10 using Git Bash (might require some extra configuration) and PowerShell (you might need to disable temporarily the security directives in order to activate the virtual environment) with Anaconda Python 3.7.

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

However, Kivy might not work as expected. There is an unresolved issue - system specific - where you might get a complain about having an old version of OpenGL or just a black window with no widgets. If that's your case, try one of the solutions suggested [here](https://stackoverflow.com/questions/52109670/cannot-display-anything-but-a-solid-color-window-with-kivy).
