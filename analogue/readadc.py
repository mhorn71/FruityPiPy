import logging
from Adafruit_ADS1x15 import ADS1x15 


## initialise logger
logger = logging.getLogger('analogue')

pga = 6144
sps = 8
adc = ADS1x15(ic=0x01)

def read():

    logger.debug("Analogue.readadc called")

    _reading = None

    try:


        b0 = int(adc.readADCSingleEnded(0, pga, sps))
        b1 = int(adc.readADCSingleEnded(1, pga, sps))
        b2 = int(adc.readADCSingleEnded(3, pga, sps))

 #       print "Reading are 0 = ", b0
 #       print "Reading are 1 = ", b1
 #       print "Reading are 2 = ", b2
 #       print "Reading are 3 = ", b3

        r0 = "{0:04d}".format(b0)
        r1 = "{0:04d}".format(b1)
        r2 = "{0:04d}".format(b2)
    except IOError:
        _reading = '0000', '0000', '0000'
        logger.debug("%s %s", "adc IO Error ", e)
    except RuntimeError:
        _reading = '0000', '0000', '0000'
        logger.debug("%s %s", "adc RuntimeError ", e)
    else:
        _reading = r0, r1, r2

    return _reading

if __name__ == "__main__":
    print read()

