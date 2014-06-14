import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging
from Adafruit_ADS1x15 import ADS1x15
import re


##initialise logger
logger = logging.getLogger('actions.getTemperature')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

pga = 6144
sps = 8
adc = ADS1x15(ic=0x01)

def control():

    logger.debug("getTemperature called")

    try:
        b0 = adc.readADCSingleEnded(3, pga, sps)
        logger.debug("%s %s", "Raw reading converted to mV ", b0)
        pretemp = (b0 - 500) / 10
        logger.debug("%s %s", "mv converted to C ((b0 - 500) / 10) ", pretemp)

        # We always want to return the following format +/-00.0
        if re.match("^\d$", str(pretemp)):  # matched 0 - 9
            temp = '+' + str(pretemp).zfill(2) + '.' + '0'
        elif re.match("^\d\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(2)
            temp = '+' + b + '.' + a[1][:1]
        elif re.match("^\d{2}$", str(pretemp)):
            temp = '+' + str(pretemp) + '.0'
        elif re.match("^\d{2}\.\d*$", str(pretemp)):
            temp = '+' + str(pretemp)[:4]
        elif re.match("^-\d$", str(pretemp)):
            a = str(pretemp).replace('-', '')
            temp = '-' + str(a).zfill(2) + '.0'
        elif re.match("^-\d{1,2}\.\d*$", str(pretemp)):
            # matched -1.8888
            a = str(pretemp).replace('-', '')
            b = str(a).split('.')
            c = b[0].zfill(2)
            temp = '-' + c + '.' + b[1][:1]
        elif re.match("-\d{2}\.\d*$", str(pretemp)):
            temp = str(pretemp)[:5]
        else:
            temp = '+00.0'

        value = temp

        logger.debug("%s %s", "getTemperature returned value ", value)
    except IOError as e:
        logger.critical("%s %s", "premature termination", e)
        status = 4
        value = e
        logger.critical("%s %s", "getTemperature premature termination", e)
    else:
        status = 0

    status = status + samplerstatus.status()

    return status, value

