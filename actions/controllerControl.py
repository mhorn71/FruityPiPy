__author__ = 'mark'
import subprocess
import utilities.samplerstatus as samplerstatus
import ConfigParser
import signal
import logging
import sys


##initialise logger
logger = logging.getLogger('actions.controllerControl')

config = ConfigParser.RawConfigParser()
#config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    status = None
    value = None

    config.read("StarinetBeagleLogger.conf")

    logger.debug("%s %s", "controllerControl buffer0 ", buffer0)

    if samplerstatus.status() == 0:
        logger.debug("%s %s", "samplerstatus reports sampler not active", str(samplerstatus.status()))
        status = 0
        if buffer0 == 'Reboot':
            return status, value
            subprocess.call("reboot")
        elif buffer == 'Shutdown':
            return status, value
            subprocess.call("shutdown", "-h", "now")
        else:
            logger.critical("%s %s", "controllerControl INVALID_PARAMETER buffer0", buffer0)
    elif samplerstatus.status() == 8000:
        logger.debug("%s %s", "samplerstatus reports sampler active", str(samplerstatus.status()))
        status = 8002
        return status, value
