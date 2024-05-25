# Roadef Scheduling
This repository contains a Python program designed for scheduling sessions for the ROADEF 2024 conference. The program encodes the problem into Linear programming  ,which can be then solved through dedicated solvers ceplex to efficiently allocate sessions while minimising working-group conflicts.

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
python3.10 -m venv ./myenv3.10CeplexNewVersion
```
# Step 3: Activate the virtual environment
```bash
source ./myenv3.10CeplexNewVersion/bin/activate
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
cd /home/mis/Bureau/ceplex_installation/cplex/python/3.10/x86-64_linux
```
# Step 7: Install the CPLEX Python API
```bash
python setup.py install
```
# Install docplex 
```bash
pip install docplex
```

# If you can't install python3.10 follow this Steps
To ensure that the `python` and `python3` commands run Python 3.10 by default, follow these steps:

## Step 1: Install Python 3.10 from Source

1. **Update package lists:**
   ```sh
   sudo apt update
   ```
## Install the required dependencies
```sh
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev
```

## Download the Python 3.10 source code:
   ```sh
   curl -O https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz

   ```
## Extract the downloaded file:
   ```sh
    tar -xf Python-3.10.0.tgz
   ```   
## Navigate to the extracted directory:
   ```sh
   cd Python-3.10.0

   ```  
## Navigate to the extracted directory:
  ```sh
   cd Python-3.10.0

   ```   
   ## Configure the build environment:
   
   ```sh
   ./configure --enable-optimizations
   ```
   ## Build and install Python:
   ```sh
   make -j $(nproc)
  sudo make altinstall

   ```
   ## Verify Python 3.10 installation:
      
   ```sh
   /usr/local/bin/python3.10 --version
   ```   

   # Step 2: Set Python 3.10 as the Default Version
   ## Add Python 3.10 to the alternatives system:
   ```sh
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 1
    sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.10 1
   ```   
   ## Update the default Python version:
   ```sh
   sudo update-alternatives --config python3
   sudo update-alternatives --config python
   ```   
   ## Create symlinks (if necessary):
   ```sh
    sudo rm /usr/bin/python
    sudo rm /usr/bin/python3
    sudo ln -s /usr/local/bin/python3.10 /usr/bin/python
    sudo ln -s /usr/local/bin/python3.10 /usr/bin/python3
   ```
   ## Verify the default Python version:
   ```sh
   python --version
   python3 --version

   ```