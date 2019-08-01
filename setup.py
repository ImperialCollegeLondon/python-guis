from setuptools import setup

setup(
    name="PythonGUIs",
    version="0.1",
    url="https://github.com/ImperialCollegeLondon/python-guis",
    author="Research Computing Service, Imperial College London",
    author_email="rcs-support@imperial.ac.uk",
    setup_requires=["pytest-runner"],
    install_requires=["kivy", "matplotlib", "numpy", "scikit-image", "scipy", "jupyter"],
    tests_require=["pytest-cov", "pytest-flake8", "pytest-mypy"],
)
