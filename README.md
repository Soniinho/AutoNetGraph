# Python Project
This is an app that lets you clone virtual machines and set up their network addresses automatically using a graphical interface.
Written by Soniinho.

## SETUP:
1) This was written in Python 3.11.1. Install page here: https://www.python.org/downloads/release/python-3111/

2) In order to use this app, you will need to install VirtualBox version 6.1.14 (the last version supported by the package "virtualbox"). You will also need to download the SDK and extract it into the project folder. Install page here: https://download.virtualbox.org/virtualbox/6.1.14/

3) Run `generate-environment.bat` on Windows or `generate-environment.sh` on Linux to generate the virtual environment and install all the modules, including the VirtualBox SDK.

## Using the App

1) Run `main.py`.

2) Once it's running, select a virtual machine from the list and click "Select Machine".

3) After that, a new window will open where you can choose to create a "Computer" or a "Gateway." You can connect them by selecting them simultaneously and clicking "Connect."

4) After creating a "Computer" or "Gateway," right-click to open a menu where you can edit the node's properties or delete it. Nodes can also be moved by selecting them with the left mouse button and dragging them.

5) Finally, you can click "Clone Machines" to start the cloning process and network address configuration, one machine at a time.

