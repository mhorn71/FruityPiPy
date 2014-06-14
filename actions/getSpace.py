import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging
import os

##initialise logger
logger = logging.getLogger('actions.getSpace')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getSpace called")

    try:
        blockcount = int(max(os.listdir(config.get("paths", "datafolder")),
                             key=lambda p: os.path.getctime(os.path.join(
                                 config.get("paths", "datafolder"), p))), 16) + 1
        value = str(int(100 - int(100 * float(blockcount) / 65534))).zfill(3)
    except ConfigParser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to open datafolder", e)
    except ValueError:
        value = '000'
        status = 0
    else:
        status = 0
        logger.debug("%s %s", "getSpace returned value ", value)
    
    status = status + samplerstatus.status()

    return status, value
