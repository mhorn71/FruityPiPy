FruityPiPy
==========

3 Channel RaspberryPi data logger for the UKRAA Starbase Observatory

Install Instructions
====================

FruityPiPy has been developed on minibian and cannot be guaranteed to work on any other OS.

    http://minibianpi.wordpress.com/

You need to install the following additional python packages.

    You can install the above using apt-get and pip as the root user or using sudo with the following commands:

    apt-get install python-smbus i2c-tools python-pip python-dev
    pip install crcmod
    pip install python-matplotlib
    pip install psutil

    read the following Adafruit article on setting up i2c on the Pi

    https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c


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