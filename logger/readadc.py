from Adafruit_ADS1x15 import ADS1x15

pga = 6144
sps = 8
adc = ADS1x15(ic=0x01)

def read():

    _reading = None

    try:

        b0 = int(adc.readADCSingleEnded(0, pga, sps))
        b1 = int(adc.readADCSingleEnded(1, pga, sps))
        b2 = int(adc.readADCSingleEnded(2, pga, sps))

        r0 = "{0:04d}".format(b0)
        r1 = "{0:04d}".format(b1)
        r2 = "{0:04d}".format(b2)

    except IOError:
        _reading = '0000', '0000', '0000'
    except RuntimeError:
        _reading = '0000', '0000', '0000'
    else:
        _reading = r0, r1, r2

    return _reading

if __name__ == "__main__":
    print read()

