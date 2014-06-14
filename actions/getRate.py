import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.getRate')

config = ConfigParser.RawConfigParser()


def control():


    logger.debug("getRate called")

    try:
        config.read("StarinetBeagleLogger.conf")
        rate = config.get("capture", "rate")
    except ConfigParser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get capture rate from config", e)
    else:
        status = 0
        value = rate.zfill(4)
        logger.debug("%s %s", "returning value ", value)
    
    status = status + samplerstatus.status()

    return status, value

