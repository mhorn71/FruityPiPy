import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.setRate')

config = ConfigParser.RawConfigParser()


def control(buffer0):

    logger.debug("setRate called")

    if samplerstatus.status() == 8000:
        status = 2
        value = None
    else:
        try:
            config.read("StarinetBeagleLogger.conf")
            config.set('capture', 'rate', buffer0)  # update
            with open('StarinetBeagleLogger.conf', 'wb') as configfile:
                config.write(configfile)
                configfile.close()
        except IOError as e:
            logger.debug("%s %s", "setRate IOError ", e)
            status = 4
            value = e
        else:
            status = 0
            value = None
    logger.debug("%s %s", "setRate returned ", status)

    status = status + samplerstatus.status()

    return status, value
