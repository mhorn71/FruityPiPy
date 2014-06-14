import re

from Adafruit_ADS1x15 import ADS1x15

pga = 6144
sps = 8
adc = ADS1x15(ic=0x01)


def read():

    try:
        b0 = adc.readADCSingleEnded(3, pga, sps)
        pretemp = (b0 - 500) / 10

        if re.match("^\d$", str(pretemp)):  # matched 0 - 9
            temp = '+' + str(pretemp).zfill(3)
        elif re.match("^\d\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(3)
            temp = '+' + str(b)
        elif re.match("^\d{2}$", str(pretemp)):
            temp = '+' + str(pretemp).zfill(3)
        elif re.match("^\d{2}\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(3)
            temp = '+' + str(b)
        elif re.match("^-\d{1,2}$", str(pretemp)):
            a = str(pretemp).replace('-', '')
            temp = '-' + str(a).zfill(3)
        elif re.match("^-\d\.\d*$", str(pretemp)):
            # matched -1.8888
            a = str(pretemp).replace('-', '')
            b = str(a).split('.')
            c = b[0].zfill(3)
            temp = '-' + c
        elif re.match("-\d{2}\.\d*$", str(pretemp)):
            a = str(pretemp).replace('-', '')
            b = str(a).split('.')
            c = b[0].zfill(3)
            temp = '-' + c
        else:
            temp = '+000'

        value = temp

    except IOError:

        value = '+000'

    return value
