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

## initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

## initialise globals
rate = int(config.get('capture', 'rate').lstrip("0"))
strrate = config.get('capture', 'rate')
datafolder = config.get("paths", "datafolder")

## initialise next_call
next_call = time.time()
lock = threading.Lock()


def mylogger():
    
    lock.acquire()

    global ptn
    global next_call
    global rate
    global datafolder
    global datafile 
    global strrate

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
                print "Unable to assign pid to pro.pid capture.py"
            else:
                try:
                    os.remove(str(config.get('paths', 'pidfile')))
                except OSError as e:
                        print "Unable to remove pid file fatal error", e
                else:
                    try:
                        os.kill(pid, signal.SIGTERM)
                    except OSError as e:
                        print "Unable to kill process logger/sampler"



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
        
    lock.release()

datafile0000 = datafolder + '0000'

print 'datafile = ', datafile0000

if os.stat(datafile0000)[6] == 0:  # check to see if first data file is zero bytes.
    print "Datafile is zero bytes"
    datafile = '0000'
    ptn = 0
    mylogger()
else:  # As first data file was zero bytes assume we're doing a restart after power outage
    print "Datafile is not zero bytes"
    # Find number of last block in data folder and increase by 1
    newblock = int(max(os.listdir(config.get("paths", "datafolder")),
                        key=lambda p: os.path.getctime(os.path.join(
                        config.get("paths", "datafolder"), p))), 16) + 1
    
    ptn = newblock  # set ptn number to last block plus one.
    print "ptn = ", str(ptn)
    datafile = str(hex(newblock).split('x')[1].upper().zfill(4))  # our new datafile in hex
    print "New data file is ", datafile 

    ###############
    # Get the lastblock written too and read block and assign to block

    lastblock = str(max(os.listdir(config.get("paths", "datafolder")),
                        key=lambda p: os.path.getctime(os.path.join(
                        config.get("paths", "datafolder"), p))))  # find the lastblock so we can extract date time str

    fileblock = open(config.get("paths", "datafolder") + lastblock, 'rb')  # open the lastblock that was written too

    block = fileblock.read().strip('\x02\x1F\x04\r\n\x00')  # read contents of datafile stripping control characters.

    fileblock.close()

    #  Assign date time string to lastdatelst list

    lastdatelst = re.findall('^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$', block)  # find date time string

    # split lastdatelst into lastdate and lasttime

    splitdatetimelst = str.split(str(lastdatelst[0]), ' ') # split lastdatelst on space

    fmtdate = splitdatetimelst[0].split('-')  # split date field on hyphen
    fmttime = splitdatetimelst[1].split(':')  # split time field on colon

    # create date time object
    lasttimestamp = datetime.datetime(int(fmtdate[0]),int(fmtdate[1]),int(fmtdate[2]),int(fmttime[0]),int(fmttime[1]),int(fmttime[2]))

    #################################################
    # increase lasttimestamp by (sample rate * 40)
    # There could be issues doing this as below as I'm not sure what would happen in the case of the day rolling over

    xtime = int(config.get('capture', 'rate').lstrip("0")) * 40
    nexttimestamp = lasttimestamp + datetime.timedelta(0, xtime)

    # get current time and check that's in excess of the nexttimestamp

    currentdatetime = datetime.datetime.now()

    while currentdatetime < nexttimestamp:
        time.sleep(xtime)
    else:
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    #
    ##################################################

    f = open(config.get("paths", "datafolder") + datafile, 'wb')

    data = str(stamp) + ' ' + temperature.read() + ' ' + strrate + '   '
    f.write(data)        
    f.close()

    mylogger()
