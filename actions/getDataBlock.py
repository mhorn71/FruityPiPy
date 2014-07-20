import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging


##initialise logger
logger = logging.getLogger('actions.getDataBlock')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    logger.debug("getDataBlock called")

    value = None

    try:
        f = open(config.get("paths", "datafolder") + str(buffer0), 'r')
        datablock = f.read().strip('\x02\x1F\x04\r\n\x00')
        f.close()
        logger.debug("%s %s", "getting data block ", buffer0)
    except IOError as e:
        status = 8
        logger.critical("%s %s", "unable to open data block", e)
    else:
        status = 0
        value = datablock.ljust(512, '0').strip('\r\n\x00')
        logger.debug("%s %s", "returning data block", buffer0)

    status = status + samplerstatus.status()

    return status, value


