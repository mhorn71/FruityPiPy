__author__ = 'mark'

import ftplib
import actions.capture as capture
import actions.capturePublisher as capturePublisher
import utilities.samplerstatus as samplerstatus
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def myDataPublisher():

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



    