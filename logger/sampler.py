__author__ = 'mark'
import ConfigParser
import datetime
import time
import os
import threading
import readadc
import temperature
import signal
import re
import logging

## initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

## initialise globals
rate = int(config.get('capture', 'rate').lstrip("0"))
strrate = config.get('capture', 'rate')
datafolder = config.get("paths", "datafolder")
index = 1

## initialise next_call
next_call = time.time()
lock = threading.Lock()

##initialise logger
## If you want to see debugging info change level=logging.CRITICAL to level=logging.DEBUG
## Make sure you change the level back to CRITICAL as logfile does not auto rotate.
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        filename=config.get('paths', 'samplerlogfile'),
                        level=logging.CRITICAL,
                        filemode='a')

logger.debug("%s %s", "Sample rate set to - ", str(rate))

def mylogger():

    lock.acquire()

    global ptn
    global next_call
    global rate
    global datafolder
    global datafile
    global strrate
    global index

    # immediately set schedule of next sample.
    next_call += rate
    threading.Timer(next_call - time.time(), mylogger).start()

    #open datafile
    f = open(datafolder + datafile, 'rb')

    #set the first sample time stamp
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    f.readline()

    if f.tell() == 0:
        f = open(datafolder + datafile, 'ab')
        samplerdata = ''.join(readadc.read())
        data = str(stamp) + ' ' + temperature.read() + ' ' + strrate + '   ' + \
            str(samplerdata)
        f.write(data)
        f.close()
    elif f.tell() == 512:
        ptn += 1
        datafile = hex(ptn).split('x')[1].upper().zfill(4)  # change filenumber to hex

        if datafile == 'FFFE':
            try:
                pidfile = open(config.get('paths', 'pidfile'), 'r')
                pid = int(pidfile.read())
                pidfile.close()
            except IOError as e:
                logger.critical("%s %s", "Unable to assign pid to pro.pid capture.py", e)
            else:
                try:
                    os.remove(str(config.get('paths', 'pidfile')))
                except OSError as e:
                        logger.critical("%s %s", "Unable to remove pid file fatal error", e)
                else:
                    try:
                        os.kill(pid, signal.SIGTERM)
                    except OSError as e:
                        logger.critical("%s %s", "Unable to kill process logger/sampler", e)



        f = open(datafolder + datafile, 'wb')
        samplerdata = ''.join(readadc.read())
        data = str(stamp) + ' ' + temperature.read() + ' ' + strrate + '   ' + \
            str(samplerdata)
        f.write(data)
        f.close()
    else:
        f = open(datafolder + datafile, 'ab')
        samplerdata = ''.join(readadc.read())
        data = str(samplerdata)
        f.write(data)
        f.close()

    logger.debug("%s %s %s %s", str(index).rjust(6, ' '), str(stamp), str(temperature.read()), str(samplerdata))
    index += 1

    lock.release()

datafile0000 = datafolder + '0000'

print 'datafile = ', datafile0000

if os.stat(datafile0000)[6] == 0:  # check to see if first data file is zero bytes.
    logger.debug("%s", "Data Block 0000 is zero bytes starting sampler")
    datafile = '0000'
    ptn = 0
    mylogger()
else:  # As first data file was zero bytes assume we're doing a restart after power outage
    logger.debug("%s", "Restart after fatal error or power outage")
    logger.debug("%s", "Data Block 0000 is not zero bytes")
    # Find number of last block in data folder and increase by 1
    newblock = int(max(os.listdir(config.get("paths", "datafolder")),
                        key=lambda p: os.path.getctime(os.path.join(
                        config.get("paths", "datafolder"), p))), 16) + 1

    ptn = newblock  # set ptn number to last block plus one.
    print "ptn = ", str(ptn)
    datafile = str(hex(newblock).split('x')[1].upper().zfill(4))  # our new datafile in hex
    logger.debug("%s %s", "Next new data block is ", datafile)

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    f = open(config.get("paths", "datafolder") + datafile, 'wb')

    data = str(stamp) + ' ' + temperature.read() + ' ' + strrate + '   '
    f.write(data)
    f.close()

    mylogger()


