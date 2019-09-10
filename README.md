# GUIs for Python - improving the accessibility of scientific software 
 
Research software has been a driving force behind the birth and rapid growth of informatics, but it was the appearance of graphic user interfaces (GUI) in the 1980s that made computers accessible to everyone. A GUI helps to reduce the learning curve for using software, increases the base of potential users and can ultimately increase citations and impact. Moreover, a well-designed GUI can perform validation and increase the robustness and reproducibility of the results, productively decoupling developers from users. 
 
This workshop will have three parts. In the first one, we will give an introduction to GUIs and review three of the most common Python packages to create them: Tkinter for the desktop, Jupyter Widgets for web and Kivy for mobile devices (45 min). The second part will be a hands-on session where attendees will go through a range of exercises to code a complete GUI using the package of their choice (90 min). The last part will provide guidance on how to plan and implement a GUI, considering users’ objectives, accessibility, gathering feedback, providing contextual help, etc. At the end of the workshop attendees will have time to come up with an actionable plan to apply these to their own research software (45 min). 

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

## Installation instructions on a fresh Ubuntu Server 18.04 system:

Run the following two lines before running the instructions above for the situation when a desktop environment is already installed. 

```bash
sudo apt update
sudo apt install lubuntu-desktop
```

The system will need to be re-started with the Desktop environment in order to run the Workshop. 