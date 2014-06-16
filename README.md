FruityPiPy
==========

3 Channel RaspberryPi data logger for the UKRAA Starbase Observatory

Install Instructions
====================

You need to install the following additional python packages.

    crcmod
    ------
    https://pypi.python.org/pypi/crcmod/1.7

    psutils
    -------
    https://code.google.com/p/psutil/

    matplotlib
    ----------
    https://github.com/matplotlib/matplotlib

    You can install the above using apt-get and pip as the root user or using sudo with the following commands:

    apt-get install python-pip
    pip install crcmod
    pip install matplotlib
    apt-get install python-dev (need to supply python.h for psutil compilation)
    pip install psutil

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
        memory/module
        memory/module/0
        memory/module/1

    3.) Start as root.

    4.) Download Starbase from ukraa.com/builds/beta and set the IP address of your
        RaspberryPi in the file FruityPiPyLogger-instrument.xml