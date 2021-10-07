# Tests for Sapog
This folder contains tests written in Python for testing Sapog.

https://github.com/Zubax/sapog

## Resolving dependencies
Pyuavcan and DSDL namespaces are needed to run the tests.

Also, it is a good idea to create a virtual environment to store installed dependency pyuavcan in:
```
python -m venv venv
. venv/bin/activate #  activating the virtual environment
```
### Downloading the UAVCAN DSDL namespaces
Go to this page:
https://github.com/UAVCAN/public_regulated_data_types and download the zip file containing code.
### Compiling namespaces
Unpack the two contained directories to a new folder. 
#### Installing Yakut
Now [Yakut](https://github.com/UAVCAN/yakut) is needed to compile the namespaces.
These packages are needed to install Yakut on Ubuntu 20.04.
```bash
sudo apt install libjack-jackd2-dev libasound2-dev
```
If pip is available then Yakut can be installed like so:
```bash
pip install yakut
```
#### Compilation step
Enter the directory you unpacked ```uavcan/``` and ```reg/``` to and then
```
yakut compile -Ocompiled uavcan/ reg/
```
The output folder is specified as ```compiled/```. Copy the resulting two folders from ```compiled/``` to ```deps/namespaces```.
### Installing [pyuavcan](https://pyuavcan.readthedocs.io/en/stable/pages/installation.html)
```sh
pip install pyuavcan[transport_can_pythoncan,transport_serial,transport_udp]
```
## Running tests
From the ```src/``` folder, in terminals, run ```python node1.py``` and ```python node2.py```

and that's it. Now some extras:
### Using Yakut to listen to test node heartbeats
```
UAVCAN__UDP__IFACE="127.0.0.1" y sub uavcan.node.Heartbeat.1.0
```
