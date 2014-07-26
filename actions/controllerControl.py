__author__ = 'mark'
import os
import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging


##initialise logger
logger = logging.getLogger('actions.controllerControl')

config = ConfigParser.RawConfigParser()
#config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    value = None

    config.read("StarinetBeagleLogger.conf")

    logger.debug("%s %s", "controllerControl buffer0 ", buffer0)

    if samplerstatus.status() == 0:
        logger.debug("%s %s", "samplerstatus reports sampler not active", str(samplerstatus.status()))
        status = 0
        if buffer0 == 'Reboot':
            os.system('reboot')
            return 0, value
        elif buffer0 == 'Shutdown':
            os.system('shutdown -h now')
            return 0, value
        else:
            logger.critical("%s %s", "controllerControl INVALID_PARAMETER buffer0", buffer0)
            return 4, value
    elif samplerstatus.status() == 8000:
        logger.debug("%s %s", "samplerstatus reports sampler active", str(samplerstatus.status()))
        status = 8002
        return status, value


