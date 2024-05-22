# Roadef Scheduling
This repository contains a Python program designed for scheduling sessions for the ROADEF 2024 conference. The program encodes the problem into Maximum Satisfiability (Max-SAT) ,which can be then solved through dedicated solvers to efficiently allocate sessions while minimising working-group conflicts.

# Installation Instructions
Your machine must be equipped with Python 3 and pip. Follow the steps below to set up the environment and install the necessary packages. It's recommended to use a virtual environment for better management of dependencies.

# Mise A jours
```bash
sudo apt update
sudo apt upgrade
```
# Step 1: Ensure Python 3.10 is installed
```bash
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev
```
# Step 2: Create a new virtual environment
```bash
python3.10 -m venv ~/myenv3.10
```
# Step 3: Activate the virtual environment
```bash
source ~/myenv3.10/bin/activate
```
# Step 4: Verify the Python version
```bash
python --version  # Should output Python 3.10.x
```
# Step 5: Install distutils if necessary
```bash
sudo apt install python3.10-distutils
```
# Step 6: Navigate to the CPLEX Python API directory
```bash
cd ~/CPLEX_Studio129/cplex/python/3.10/x86-64_linux
```
# Step 7: Install the CPLEX Python API
```bash
python setup.py install
```