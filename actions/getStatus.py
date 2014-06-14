import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.getStatus')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2):  # buffer0 = reponse_command, buffer1 = response_status, buffer2 = response_crc

    logger.debug("%s %s %s %s", "getStatus called", buffer0, buffer1, buffer2)

    #status_code = {'0000': 'SUCCESS',
    #               '0001': 'TIMEOUT',
    #               '0002': 'ABORT',
    #               '0004': 'PREMATURE_TERMINATION',
    #               '0008': 'INVALID_PARAMETER',
    #               '0010': 'INVALID_MESSAGE',
    #               '0020': 'INVALID_COMMAND',
    #               '0040': 'INVALID_MODULE',
    #               '0080': 'INVALID_INSTRUMENT',
    #               '0200': 'CRC_ERROR',
    #               '0400': 'INVALID_XML',
    #               '8000': 'CAPTURE_ACTIVE'}

    if buffer0 is not None:
        basecommand = buffer0[2:]
        command = basecommand[:4]
        commandvariant = basecommand[4:]
        #print "getStatus buffer 0 stripped of address ", basecommand 
        #print "getStatus basecommand stripped of command variant ", command 
        #print "getStatus basecommand stripped of code base and command ", commandVariant 
        #print "getStatus response status of last command ", buffer1
        #print "getStatus response crc of last command ", buffer2 
        value = command + ' ' + commandvariant + ' ' + buffer1 + ' ' + buffer2
    else:
        value = '0000 0000 0000 0000'

    status = 0
 
    logger.debug("%s %s", "getStatus returned ", value)

    status = status + samplerstatus.status()

    return status, value
