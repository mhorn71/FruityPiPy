import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging
import socket

##initialise logger
logger = logging.getLogger('actions.getHostname')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getHostname called")

    try:
        value = socket.gethostname()
    except StandardError as e:
        status = 4
        value = e
        logger.critical("%s %s", "failure to get gethostname() ", e)
    else:
        status = 0
        
    logger.debug("%s %s", "getHostname returned ", value)

    status = status + samplerstatus.status()

    return status, value
