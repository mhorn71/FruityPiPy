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
datafile = '0000'

## initialise next_call
next_call = time.time()
lock = threading.Lock()

ptn = 0


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
                    os.kill(pid, signal.SIGTERM)
                except OSError as e:
                    print "Unable to kill process logger/sampler"
                else:
                    try:
                        os.remove(str(config.get('paths', 'pidfile')))
                    except OSError as e:
                        print "Unable to remove pid file fatal error", e

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


mylogger()
