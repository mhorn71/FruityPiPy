FruityPiPy
==========

3 Channel RaspberryPi data logger for the UKRAA Starbase Observatory

Install Instructions
====================

FruityPiPy has been developed on Raspbian and cannot be guaranteed to work on any other OS.

    http://www.raspberrypi.org/downloads/

You need to install the following additional python packages.

    You can install the above using apt-get and pip as the root user or using sudo with the following
    commands:

    apt-get install python-smbus i2c-tools python-pip python-dev libpng12-dev
    pip install crcmod
    pip install psutil

Add the following two lines to /etc/modules and then reboot the Pi.

    i2c-bcm2708
    i2c-dev

Matplotlib and the Raspberry Pi.

    Please note the default package for matplotlib currently in the Raspbian repositories is out of date
    and broken, you will need to build matplotlib 1.2.1 from source which can be obtained from
    http://matplotlib.org/downloads.html follow the instructions provided.  If you require additional help
    please ask on the BAA Radio Astronomy Group Yahoogroup.

The RaspberryPi comes without an ADC, I used the ADS1115 from Adafruit.

    ADS1115
    -------
    http://www.adafruit.com/products/1085

You will need to attach the following temperature sensor to channel 3 of the ADC.

    TMP36 Temperature Sensor
    ------------------------
    https://learn.adafruit.com/measuring-temperature-with-a-beaglebone-black/wiring

Software install

    1.) place all files in there own folder

    2.) create the following folders in the folder you extract the code too.
        run
        memory/data

    3.) Start as root.

    4.) Download Starbase from ukraa.com/builds/beta and set the IP address of your
        RaspberryPi in the file FruityPiPyLogger-instrument.xml