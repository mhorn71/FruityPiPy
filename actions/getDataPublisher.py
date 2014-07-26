import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.getDataPublisher')

config = ConfigParser.RawConfigParser()


def control():

    logger.debug("getDataPublisher called")

    try:
        config.read("StarinetBeagleLogger.conf")
        interval = config.get("datapublisher", "interval")
        server = config.get("datapublisher", "server")
        username = config.get("datapublisher", "username")
        password = config.get("datapublisher", "password")
        remotefolder = config.get("datapublisher", "remotefolder")
    except ConfigParser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get dataPublisher parameters from config", e)
    else:
        status = 0
        value = str(interval) + ',' + server + ',' + username + ',' + password + ',' + str(remotefolder)
        logger.debug("%s %s", "returning value ", value)

    status = status + samplerstatus.status()

    return status, value
