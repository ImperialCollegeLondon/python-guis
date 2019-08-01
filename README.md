# python-guis

Installation instructions on a fresh Lubuntu 18.04 system:

```bash
sudo apt update
sudo apt install git python3-venv python3-tk
git clone https://github.com/ImperialCollegeLondon/python-guis.git
cd python-guis
python3 -mvenv venv
. venv/bin/activate
pip install -U setuptools wheel pip
pip install -e .
garden install matplotlib
```
