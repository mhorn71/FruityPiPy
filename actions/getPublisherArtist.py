__author__ = 'mark'
import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.getPublisherArtist')

config = ConfigParser.RawConfigParser()


def control():

    logger.debug("getPublisherArtist called")

    try:
        config.read("StarinetBeagleLogger.conf")
        chart = config.get("publisherartist", "chart")
        channel0 = config.get("publisherartist", "channelArt0")
        channel1 = config.get("publisherartist", "channelArt1")
        channel2 = config.get("publisherartist", "channelArt2")
        temperature = config.get("publisherartist", "TemperatureArt")
    except ConfigParser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get publisher artist parameters from config", e)
    else:
        status = 0
        value = chart + ',' + channel0 + ',' + channel1 + ',' + channel2 + ',' + temperature
        logger.debug("%s %s", "returning value ", value)

    status = status + samplerstatus.status()

    return status, value
