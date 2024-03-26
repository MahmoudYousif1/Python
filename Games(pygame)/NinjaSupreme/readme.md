# Guide

To run the program, you need to use the `make` command. This command looks for a file named `Makefile` in your directory, and then runs the instructions within it. If you're having problems, make sure you're in the correct directory and that a `Makefile` exists there.

If you are having problems, try running these commands: 

## Windows
### Pip installation:
1. Download the [get-pip.py](https://bootstrap.pypa.io/get-pip.py) file to your local drive.
2. Open a command prompt and navigate to the folder containing `get-pip.py`.
3. Run the following command: `python get-pip.py`
4. Verify the installation by running: `pip --version`

### Pygame installation:
1. Open a command prompt.
2. Run the following command to install pygame: `pip install pygame`
3. Pygame is now installed! You can verify the installation by running a Python interpreter and typing: `import pygame`


## Linux
### Pip installation:
1. Open a terminal.
2. Run the following command to install pip: `sudo apt install python3-pip`
3. Verify the installation by running: `pip3 --version`

### Pygame installation:
1. Open a terminal.
2. Run the following command to install pygame: `python3 -m pip install pygame`


## Mac
### Pip installation:
1. Open a terminal.
2. Run the following command to download the `get-pip.py` file and install pip: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py`
3. Verify the installation by running: `pip3 --version`

### Pygame installation:
1. Open a terminal.
2. Run the following command to install pygame: `python3 -m pip install pygame`
3. Pygame is now installed! You can verify the installation by running a Python interpreter and typing: `import pygame`