# AutoNetGraph
This is an app that lets you clone virtual machines and set up their network addresses automatically using a graphical interface.
Written by Matheus H. Daltroso.

## SETUP:
1) This was written in Python 3.11.1. Install page here: https://www.python.org/downloads/release/python-3111/

2) In order to use this app, you will need to install VirtualBox version 6.1.14 (the last version supported by the package "virtualbox"). You will also need to download the SDK and extract it into the project folder. Install page here: https://download.virtualbox.org/virtualbox/6.1.14/

3) You will need a linux virtual machine on VirtualBox with 2 interfaces on Bridge mode, the configuration process works by login on the machine with the root user, (default being user:root password:root). It is configured by changing the keyboard layout to "us", typing everything, changing it back to "br" and then powering off the machine. You can change these on the virtualbox_manual_ct.py file.

4) Run `generate-environment.bat` on Windows or `generate-environment.sh` on Linux to generate the virtual environment and install all the modules, including the VirtualBox SDK.

## Using the App

1) Run main.py.

2) Once it's running, select a virtual machine from the list and click "Select Machine."

3) After that, a new window will open where you can choose to create a "Computer" or a "Gateway." You can connect them by selecting them simultaneously and clicking "Connect."

4) After creating a "Computer" or "Gateway," right-click to open a menu where you can edit the node's properties or delete it. Nodes can also be moved by selecting them with the left mouse button and dragging them.

5) Nodes can be connected by selecting 2 of them with CTRL + left mouse button. After clicking the "Connect" button, a window will open allowing you to choose the interface to be connected. You can also delete the connection by right-clicking on it.

6) You can also configure the network automatically, but for that you must have a root node gateway, which should only have connections using the enp0s3 interface.

7) Finally, you can click "Clone Machines" to start the cloning process and network address configuration, the function will configure all the nodes, cloning one machine at a time, starting it, configuring it and then shutting it down.
