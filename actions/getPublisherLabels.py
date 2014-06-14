__author__ = 'mark'
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
        channel0 = config.get("publisherlabels", "channel0")
        channel1 = config.get("publisherlabels", "channel1")
        channel2 = config.get("publisherlabels", "channel2")
    except ConfigParser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get publisher parameters from config", e)
    else:
        status = 0
        value = channel0 + ',' + channel1 + ',' + channel2
        logger.debug("%s %s", "returning value ", value)

    status = status + samplerstatus.status()

    return status, value
