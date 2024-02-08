#!/bin/bash

# Install clingo and graphviz using conda
echo "Installing clingo and graphviz"
sudo apt-get install graphviz graphviz-dev --yes
sudo apt install gringo --yes

# install clingo python package and pandas
pip install clingo
pip install pandas

# Reset Jupyter Kernel
jupyter kernelspec uninstall python3 --yes
/home/codespace/.python/current/bin/python -m ipykernel install --user --name=python3

echo "Setup completed successfully"