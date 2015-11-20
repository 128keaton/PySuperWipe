# PySuperWipe
A python script for erasing Cisco 1800 series routers
# Usage
Plug router into serial port, note port 
Run:
	wget https://goo.gl/gPVncz && sudo python reset.py -p /dev/ttyS0 -d False

* -p is the port (/dev/ttyS0)
* -d  is debug (True/False)


## Setup:

### Linux:
It works, as is, with most, if not all, modern Linux installs.
	
### OS X:
First, install this (http://changux.co/osx-installer-to-pl2303-serial-usb-on-osx-lio/)[serial port driver] for OS X.
Then, install serial from pip.
	`
	$ curl -O http://python-distribute.org/distribute_setup.py
	$ sudo python distribute_setup.py
	$ curl -O https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
	$ sudo python get-pip.py
	
and then just run like normal.
	`wget https://goo.gl/gPVncz && sudo python reset.py -p /dev/ttyS0 -d False`
Note: you might have to unplug and replug the serial adaptor (in the same USB port) to get it to work.
	
	
### Winders:
To be announced!