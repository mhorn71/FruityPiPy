__author__ = 'mark'

import ftplib
import actions.capture as capture
import actions.capturePublisher as capturePublisher
import utilities.samplerstatus as samplerstatus
import utilities.publisherstatus as publisherstatus
import ConfigParser
import os, os.path
import datetime

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def myDataPublisher():

    if config.get('systemstate', 'datapublisher') == 'true':

        # Check to see if capturePublisher is running if it is stop it.

        if publisherstatus.status() == 0:  # if capturePublisher active true
            config.set('systemstate', 'datapublisherpub', 'true')
            with open('StarinetBeagleLogger.conf', 'wb') as configfile:
                    config.write(configfile)
                    configfile.close()
            capPub = 1
            capturePublisher.control('false')
        else:
            config.set('systemstate', 'datapublisherpub', 'false')
            with open('StarinetBeagleLogger.conf', 'wb') as configfile:
                    config.write(configfile)
                    configfile.close()
            capPub = 0

        # Check to see if capture is running which is should be and stop it.
        if samplerstatus.status() == 8000:  # if capture active true
            capture.control('false')



    def myftp(filename):
        try:
            session = ftplib.FTP(config.get('datapublisher', 'server'),config.get('datapublisher', 'username'),
                                 config.get('datapublisher', 'password'))
            session.cwd(config.get('datapublisher', 'remotefolder'))  # Change directory
            fd=open(filename,'rb')  # file to send
            session.storbinary("STOR %s" % filename, fd)    # send the file
            file.close()                                    # close file and FTP
            session.quit()
        except ftplib.all_errors as e:
            print "We had an FTP Error - ", e


    # Format date and time for RawData filename
    # Change this to get date and time from block 0000
    daystamp = datetime.datetime.now().strftime("%Y%m%d")
    timestamp = datetime.datetime.now().strftime("%H%M%S")

    # Create filename for RawData
    filename = 'RawData_' + str(daystamp) + '_' + str(timestamp) + '.csv'
    # filename format RawData_20140726_230300.csv

    # Copy metadata into new filename

    with open("instrument.metadata") as f:
        with open(filename, "w") as f1:
            for line in f:
                if "ROW" in line:
                    f1.write(line)
        f1.close()
        f.close()

    with open("observer.metadata") as f:
        with open(filename, "a") as f1:
            for line in f:
                if "ROW" in line:
                    f1.write(line)
        f1.close()
        f.close()

    with open("observatory.metadata") as f:
        with open(filename, "a") as f1:
            for line in f:
                if "ROW" in line:
                    f1.write(line)
        f1.close()
        f.close()


    len(list) # will print number of items in list
    # This will print number of file in folder: print len([name for name in os.listdir('.') if os.path.isfile(name)])
