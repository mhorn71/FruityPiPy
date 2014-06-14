import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.getPublisher')

config = ConfigParser.RawConfigParser()


def control():

    logger.debug("getPublisher called")

    try:
        config.read("StarinetBeagleLogger.conf")
        interval = config.get("publisher", "interval")
        server = config.get("publisher", "server")
        username = config.get("publisher", "username")
        password = config.get("publisher", "password")
        remotefolder = config.get("publisher", "remotefolder")
    except ConfigParser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get publisher parameters from config", e)
    else:
        status = 0
        value = str(interval) + ',' + server + ',' + username + ',' + password + ',' + str(remotefolder)
        logger.debug("%s %s", "returning value ", value)

    status = status + samplerstatus.status()

    return status, value
