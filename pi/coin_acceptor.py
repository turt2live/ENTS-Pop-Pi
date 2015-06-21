import serial
import RPi.GPIO as GPIO

class CoinAcceptor:
    # Reads from the sparkfun 6-coin acceptor
    # (sparkfun part COM-11636, model DG600F(S))

    # Coin reader configuration: 0011 (DIP switches)

    __comPort = '/dev/ttyAMA0' # TODO: Configuration variable
    __inhibitPin = 12 # Board number # TODO: Configuration value
    __inhibited = False

    def __init__(self):
        self.__serial = serial.Serial(
            port = self.__comPort,
            baudrate = 9600,
            parity = serial.PARITY_EVEN,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = None # Wait forever
        )
        self.__serial.flush()
        print("Coin acceptor connected to serial port " + self.__serial.portstr)
        GPIO.setup(self.__inhibitPin, GPIO.OUT)
        GPIO.output(self.__inhibitPin, GPIO.HIGH)
        print("Coin acceptor inhibit pin configured")
        self.inhibit(True)

    def inhibit(self, setInhibited):
        if setInhibited == self.__inhibited:
            return # Nothing to change
        self.__inhibited = setInhibited
        if not setInhibited:
            GPIO.output(self.__inhibitPin, GPIO.LOW)
            self.__serial.flush()
            print("Coin acceptor not inhibited")
        else:
            GPIO.output(self.__inhibitPin, GPIO.HIGH)
            print("Coin acceptor inhibited")

    def readCoin(self):
        self.__serial.flush()
        coin = ""
        while coin is None or len(coin) <= 0:
            coin = self.__serial.read()
        readValue = ord(coin[0]) # Only care about first character (byte)
        centValue = -1
        # TODO: Convert this if-else ladder to a configuration for the coin reader
        if readValue == 0x0A:
            centValue = 25
        elif readValue == 0x14:
            centValue = 100
        elif readValue == 0x1E:
            centValue = 200
        if centValue < 0:
            raise ValueError("Cent value " + str(centValue) + " is not valid (raw = " + str(readValue) + ")")
        return centValue

    def shutdown(self):
        self.__serial.close()
        print("Coin acceptor shut down")
