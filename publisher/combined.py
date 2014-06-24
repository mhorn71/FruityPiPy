__author__ = 'mark'
import matplotlib

matplotlib.use('Agg')  ## do this before import matplotlib.pyplot so tkinter doesn't cause an error.

import matplotlib.pyplot as plt
import os
import time
import ConfigParser
import re
import datetime
import threading
import ftplib
import gc
from matplotlib.ticker import MaxNLocator


config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

label0 = config.get("publisherlabels", "channel0")
label1 = config.get("publisherlabels", "channel1")
label2 = config.get("publisherlabels", "channel2")

art0 = config.get("publisherartist", "channelArt0")
art1 = config.get("publisherartist", "channelArt1")
art2 = config.get("publisherartist", "channelArt2")
art3 = config.get("publisherartist", "temperatureArt")

samplerate = int(config.get('capture', 'rate').lstrip("0"))

row = 0

if art0 == 'true':
    row += 1
    ann = row

if art1 == 'true':
    row += 1
    bnn = row

if art2 == 'true':
    row += 1
    cnn = row

if art3 == 'true':
    row += 1
    enn = row


## initialise next_call
next_call = time.time()


def mypublisher():

    # set channel labels from globals
    global label0
    global label1
    global label2
    global art0
    global art1
    global art2
    global art3
    global samplerate
    global row
    global ann
    global bnn
    global cnn
    global enn

    #immediatly set schedule of next sample.
    global next_call
    interval = int(config.get('publisher', 'interval').lstrip("0"))
    #print "Interval set to - ", interval
    rate = interval * 60
    #print "Rate has been converted to seconds - ", rate
    next_call += rate
    threading.Timer(next_call - time.time(), mypublisher).start()

    #print "yep we got to _type function"

    # set channel arrays
    channel0 = []
    channel1 = []
    channel2 = []
    temperature = []
    sampletime = []

    def myftp():
        try:
            session = ftplib.FTP(config.get('publisher', 'server'),config.get('publisher', 'username'),
                                 config.get('publisher', 'password'))
            session.cwd(config.get('publisher', 'remotefolder')) # Change directory
            file = open('chart.png','rb')                  # file to send
            session.storbinary('STOR chart.png', file)     # send the file
            file.close()                                    # close file and FTP
            session.quit()
        except ftplib.all_errors as e:
            print "We had an FTP Error - ", e
        else:
            gc.collect()

    # combined chart
    def combined(sampletime,channel0,channel1,channel2,temperature):

        # print "Combined chart routine run"

        try:
            # initialise plt
            fig, ax1 = plt.subplots(figsize=(10,5))

            # plot channels
            if art0 == 'true':
                ax1.plot(sampletime, channel0, 'b-', label=label0)

            if art1 == 'true':
                ax1.plot(sampletime, channel1, 'g-', label=label1)

            if art2 == 'true':
                ax1.plot(sampletime, channel2, 'c-', label=label2)

            ax1.set_xlabel('Time (UTC)')
            ax1.set_ylabel('mV')
            ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax1.set_ylim(0, 5000)

            if art3 == 'true':
                ax2 = ax1.twinx()
                ax2.plot(sampletime, temperature, 'r-', label='Temp')
                ax2.set_ylabel('Celsius')
                ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax2.margins(0, 1)

            # show legend
            ax1.legend(loc = 'upper left')

            if art3 == 'true':
                ax2.legend(loc = 'upper right')

            # auto format date axis
            fig.autofmt_xdate()

            # set grid
            plt.grid()

            # set tight layout
            #plt.tight_layout(pad=3.00,pad_w=float)

            #plt.show()
            plt.savefig("chart.png")

            # clear last figure clf() see if it helps with memory usage.
            #fig.clf()

            # close all figures to see if it helps with memory?
            plt.close('all')

        except Exception as e:
            print "We had a matplotlib error - ", e
        else:
            myftp()

    # stacked chart


    def stacked(sampletime,channel0,channel1,channel2,temperature):

        try:
            if row == 1:
                plt.figure(figsize=(7, 2.2), dpi=70)
            elif row == 2:
                plt.figure(figsize=(7, 4.4), dpi=70)
            elif row == 3:
                plt.figure(figsize=(7, 6.6), dpi=70)
            elif row == 4:
                plt.figure(figsize=(7, 8.8), dpi=70)

            #print "sampletime - ", sampletime

            # Channels
            if art0 == 'true':
                ax1 = plt.subplot(row, 1, ann)
                ax1.plot_date(sampletime, channel0, 'b-')
                ax1.set_title(label0)
                ax1.set_xlabel("Time (UTC)")
                ax1.set_ylabel("mV")
                ax1.set_ylim(0,5000)
                ax1.set_yticks((0, 1000, 2000, 3000, 4000, 5000))
                plt.xticks(rotation=30)

            if art1 == 'true':
                ax2 = plt.subplot(row, 1, bnn)
                ax2.plot_date(sampletime, channel1, 'g-')
                ax2.set_title(label1)
                ax2.set_xlabel("Time (UTC)")
                ax2.set_ylabel("mV")
                ax2.set_ylim(0,5000)
                ax2.set_yticks((0, 1000, 2000, 3000, 4000, 5000))
                plt.xticks(rotation=30)

            if art2 == 'true':
                ax3 = plt.subplot(row, 1, cnn)
                ax3.plot_date(sampletime, channel2, 'c-')
                ax3.set_title(label2)
                ax3.set_xlabel("Time (UTC)")
                ax3.set_ylabel("mV")
                ax3.set_ylim(0,5000)
                ax3.set_yticks((0, 1000, 2000, 3000, 4000, 5000))
                plt.xticks(rotation=30)

            if art3 == 'true':
                ax4 = plt.subplot(row, 1, enn)
                ax4.plot_date(sampletime, temperature, 'r-')
                ax4.set_title("Instrument Temperature")
                ax4.set_xlabel("Time (UTC)")
                ax4.set_ylabel("Celsius")
                ax4.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax4.margins(0, 1)
                plt.xticks(rotation=30)


            plt.tight_layout()

            #plt.show()
            plt.savefig("chart.png")

            # experimental plt.clf() see if it helps with memory usage.
            plt.clf()

            # experimental plt.close see if it helps with memory?
            plt.close('all')
        except Exception as e:
            print "stacked Exception - ", e
        else:
            myftp()

    # find all files in memory/data and get creation time

    def get_information(directory):
        #print "Find all files created in last 24 hours in ", directory
        file_list = []
        for i in os.listdir(directory):
            ##print "os.listdir reports ", i
            a = str(os.path.join(directory,i))
            ##print "os.path.join report ", a
            file_list.append([a,os.path.getctime(a)])  #[file,created]
            ##print "file_list data is ", file_list
            file_list.sort()
        return file_list

    for _file in get_information(config.get('paths', 'datafolder')):

        #print "_file is set to ", _file

        timenow = time.time()  # get the current Unix time
        timespan = 86400  # time in seconds (24 Hours) of chart
        dawn = timenow - timespan  # start Unix time of chart

        #print "time now ", timenow
        #print "time span ", timespan
        #print "dawn ", dawn
        #print "file[0] ", _file[0]
        #print "file[1] ", _file[1]

        if float(_file[1]) >= dawn:
            block = open(_file[0]).readline().split(' ')

            #print "block ", block

            # create datetime object
            n = str(block[0]).split('-')  # split date field up
            b = str(block[1]).split(':')  # split time field up
            dt = datetime.datetime(int(n[0]),int(n[1]),int(n[2]),int(b[0]),int(b[1]),int(b[2]))

            #dt = str(block[0]) + ',' + str(block[1])

            #print "dt set to ", dt
            ##print "block[6] ", block[6]

            for datum in re.findall('\d{12}', block[6]):  # for every group of 16 digits
                dat = re.findall('....', str(datum))   # split each 16 digits into groups of 4
                sampletime.append(dt)  # append current datetime object to sampletime
                #print "date set to - ", dt
                channel0.append(int(dat[0]))  # append data to channel arrays
                channel1.append(int(dat[1]))
                channel2.append(int(dat[2]))
                temperature.append(block[2])  # append temperature to temperature array
                #print "temperature set to - ", block[2]

                dt = dt + datetime.timedelta(seconds=samplerate)  # create next sample datetime object based on get.config rate
                #print "New dt is set to - ", dt

    if config.get('publisherartist', 'chart') == 'combined':
        combined(sampletime,channel0,channel1,channel2,temperature)
    elif config.get('publisherartist', 'chart') == "stacked":
        stacked(sampletime,channel0,channel1,channel2,temperature)


mypublisher()
