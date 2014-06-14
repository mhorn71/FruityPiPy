import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging
import re
import uuid

##initialise logger
logger = logging.getLogger('actions.getMACAddress')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getMACAddress called")

    try:
        value = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except StandardError as e:
        status = 4
        value = e
        logger.critical("%s %s", "failure to get uuid.getnode() ", e)
    else:
        status = 0

    logger.debug("%s %s", "getMACAddress returned ", value)

    status = status + samplerstatus.status()

    return status, value
