import os
import psutil
import ConfigParser
import logging

logger = logging.getLogger('utilities.datapublisherstatus')

##initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

## the following status will return: 1 = Not Running, 0 = Running, 2 = Error

def status():

    pidfile = config.get('datapublisher', 'pidfile')

    value = None

    logger.debug("%s %s", "pidfile", pidfile)

    try:
        f = open(pidfile, 'r')
        p = int(f.readline())
        logger.debug("%s %s", "pid number", p)
        proc = psutil.Process(p)
        f.close()
    except IOError:
        logger.error("No pidfile present")
        value = 1
    except psutil.NoSuchProcess:
        logger.error("psuti.Process returned no pidfile")
        value = 1
    except ValueError as e:
        logger.error("psuti.Process returned no value from pidfile")
        os.remove(config.get('datapublisher', 'pidfile'))
        value = 1
    else:
        logger.debug("%s %s", "proc.cmdline reports ", proc.cmdline())
        try:
            b = proc.cmdline()[1]
        except IndexError as e:
            logger.error("proc.cmdline returned no value from pidfile")
            os.remove(config.get('datapublisher', 'pidfile'))
            value = 1
        else:
            if b == 'datapublisher/datapublisher.py':
                if proc.status == psutil.STATUS_ZOMBIE:
                    try:
                        os.remove(config.get('datapublisher', 'pidfile'))
                    except IOError as e:
                        logger.error("%s %s", "Unable to remove pid file fatal error", e)
                        value = 2
                else:
                    value = 0
            else:
                try:
                    os.remove(config.get('datapublisher', 'pidfile'))
                except IOError as e:
                    logger.error("%s %s", "Unable to remove pid file fatal error", e)
                    value = 2
                else:
                    value = 0

        logger.debug("%s %s", "Status = ", str(value))

    return value
