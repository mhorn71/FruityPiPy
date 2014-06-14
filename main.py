import socket
import threading
import Queue
import interpreter
import logging
import logging.config
import ConfigParser
import time

## initialise logger
logging.config.fileConfig('StarinetBeagleLogger.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')

##initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

mybuffer = 570
my_queue = Queue.Queue()


class ReadFromUDPSocket(threading.Thread):

    def __init__(self, my_queue):
        logger.info("ReadFromUDPSocket __init__ initialised.")
        threading.Thread.__init__(self)
        self.my_queue = my_queue

    def run(self):
        logger.debug("ReadFromUDPSocket run initialised.")
        while True:
            buffer1, addr = socketUDP.recvfrom(mybuffer)
            logger.debug("%s %s", "received data - ", repr(buffer1))

            if buffer1.startswith('\x02') and buffer1.endswith('\x04\r\n'):
                logger.debug("%s %s %s",  'Starinet UDP Packet received from', addr, repr(buffer1))
                self.my_queue.put((buffer1, addr))
                self.my_queue.join()


class Process(threading.Thread):

    def __init__(self, my_queue):

        logger.info("Process __init__ initialised.")

        threading.Thread.__init__(self)
        self.my_queue = my_queue
        self.alive = threading.Event()
        self.alive.set()

    def run(self):

        logger.debug("Process run initialised.")

        while True:
            buffer3 = self.my_queue.get()
            x = interpreter.processor(buffer3[0])

           # print "Interpreter returned - ", repr(x)

            if x is not None:
                #buffer4 = '\x0200000100000000127A\x04\r\n'  # Temp line just for testing.
                buffer4 = x
                logger.debug("%s %s", "return data ", repr(buffer4))
                socketUDP.sendto(buffer4, buffer3[1])
                self.my_queue.task_done()
            else:
                print "x has no data"
                self.my_queue.task_done()


if __name__ == '__main__':

    # Create socket (IPv4 protocol, datagram (UDP)) and bind to address
    try:
        socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socketUDP.bind((config.get("network", "ip"), int(config.get("network", "port"))))
    except socket.error:
        logger.critical("Fatal Error unable to open network port.")
        exit(1)
    else:
        logger.info("%s %s", "Initiated IPv4 Socket bound to port ", config.get("network", "port"))

    # Instantiate & start threads
    myServer = ReadFromUDPSocket(my_queue)
    myInterpreter = Process(my_queue)
    myServer.setDaemon(True)
    myInterpreter.setDaemon(True)

    myServer.start()
    myInterpreter.start()

    while 1:
        time.sleep(1)

    socketUDP.close()
