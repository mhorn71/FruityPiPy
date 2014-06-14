import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging
import logger.readadc as readadc

##initialise logger
logger = logging.getLogger('actions.getA2D')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    logger.debug("%s %s", "getA2D called", buffer0)

    try:
        value = readadc.read()[int(buffer0)]
        logger.debug("%s %s", "getA2D returned value ", value)
    except IOError as e:
        logger.critical("%s %s", "premature termination", e)
        status = 4
        value = None
    except IndexError as e:
        logger.critical("invalid parameter")
        status = 8
        value = None
    else:
        status = 0

    status = status + samplerstatus.status()

    return status, value
