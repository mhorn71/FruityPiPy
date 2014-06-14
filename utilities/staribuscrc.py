__author__ = 'mark'
import crcmod
import logging
import sys


## Set crc16 parameters to polynomial 8408, initial value 0xffff, reversed True, Final XOR value 0x00
crc16 = crcmod.mkCrcFun(0x018408, 0xFFFF, True, 0x0000)

## initialise logger
logger = logging.getLogger('utilities.staribuscCrc')


def checkcrc(buffer0):

    logger.debug("Check crc was called.")

    rxcrc = buffer0.strip('\x02\x04\r\n')[-4:]  # assign the received crc to rxcrc

    logger.debug("%s %s", "Received data crc - ", rxcrc)

    newrxcrc = str(hex(crc16(buffer0.strip('\x02\x04\r\n')[:-4])).replace('x', '')[1:].zfill(4)).upper()  # new crc

    logger.debug("%s %s", "Calculated new crc based on received data -", newrxcrc)

    #### Check old and new crc's match if they don't return string with 0200 crc error
    if newrxcrc != rxcrc:
        logger.debug("%s %s %s %s", "Received crc - ", rxcrc, "does not match our generated crc - ", newrxcrc)
        return '0200'
    else:
        logger.debug("CRC' match")
        return '0'


def newcrc(buffer0):

    logger.debug("New crc was called.")

    datacrc = str(hex(crc16(buffer0)).replace('x', '')[1:].zfill(4)).upper()
    value = datacrc
    logger.debug("%s %s", "Calculated new message crc -", datacrc)

    return value


if __name__ == "__main__":
    print newcrc(str(sys.argv[1:]))
