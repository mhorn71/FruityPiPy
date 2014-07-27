__author__ = 'mark'
import ConfigParser
import datetime
import time
import os
import threading
import readadc
import temperature
import signal

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
    lastblock = int(max(os.listdir(config.get("paths", "datafolder")),
                        key=lambda p: os.path.getctime(os.path.join(
                        config.get("paths", "datafolder"), p))), 16) + 1
    
    ptn = lastblock  # set ptn number to last block plus one.
    print "ptn = ", str(ptn)
    datafile = str(hex(lastblock).split('x')[1].upper().zfill(4))  # our new datafile in hex
    print "New data file is ", datafile 

    ###############
    # This next bit is wrong but works kind of.
    # I need to open the last data file and get the time and then work out when
    # to schedule the next sample to ensure we don't have data overlap based on the sample rate.

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    ###############

    f = open(config.get("paths", "datafolder") + datafile, 'wb')

    data = str(stamp) + ' ' + temperature.read() + ' ' + strrate + '   '
    f.write(data)        
    f.close()

    mylogger()
