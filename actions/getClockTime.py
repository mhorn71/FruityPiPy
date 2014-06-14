import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging
import datetime

##initialise logger
logger = logging.getLogger('actions.getClockTime')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():
    
    logger.debug("getClockTime called")

    try:
        value = datetime.datetime.now().strftime("%H:%M:%S")
    except StandardError as e:
        logger.critical("%s %s", "premature termination", e)
        value = e
        status = 4
    else:
        status = 0
        
    logger.debug("%s %s", "getClockTime returned ", value)

    status = status + samplerstatus.status()

    return status, value
