from setuptools import setup
from pathlib import Path

with Path("requirements.txt").open("r") as f:
    dependencies = f.readlines()

setup(
    name="PythonGUIs",
    version="0.2",
    url="https://github.com/ImperialCollegeLondon/python-guis",
    author="Research Computing Service, Imperial College London",
    author_email="rcs-support@imperial.ac.uk",
    install_requires=dependencies,
)