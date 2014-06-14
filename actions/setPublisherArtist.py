__author__ = 'mark'
import utilities.publisherstatus as publisherstatus
import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.setPublisherArtist')

config = ConfigParser.RawConfigParser()


def control(buffer0, buffer1, buffer2, buffer3, buffer4):

    logger.debug("setPublisherArtist called")
    logger.debug("%s %s %s %s %s", buffer0, buffer1, buffer2, buffer3, buffer4)

    if publisherstatus.status() == 0:
        status = 2  # ABORT
        value = 'capturePublisher_ACTIVE'
    else:
        try:
            config.read("StarinetBeagleLogger.conf")
            config.set('publisherartist', 'chart', buffer0)  # update
            config.set('publisherartist', 'channelArt0', buffer1)  # update
            config.set('publisherartist', 'channelArt1', buffer2)  # update
            config.set('publisherartist', 'channelArt2', buffer3)  # update
            config.set('publisherartist', 'temperatureArt', buffer4)  # update
            with open('StarinetBeagleLogger.conf', 'wb') as configfile:
                config.write(configfile)
                configfile.close()
        except IOError as e:
            logger.debug("%s %s", "setPublisherArtist IOError ", e)
            status = 4  # PREMATURE_TERMINATION
            value = e
        else:
            status = 0  # SUCCESS
            value = None
    logger.debug("%s %s", "setPublisherArtist returned ", status)

    status = status + samplerstatus.status()

    return status, value

