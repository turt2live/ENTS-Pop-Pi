import serial
import RPi.GPIO as GPIO

class CoinAcceptor:
    # Reads from the sparkfun 6-coin acceptor
    # (sparkfun part COM-11636, model DG600F(S))

    # Coin reader configuration: 0011 (DIP switches)

    __inhibited = False

    def __init__(self, comPort, inhibitPin, coinMap):
        self.__inhibitPin = inhibitPin
        self.__coinMap = coinMap
        self.__serial = serial.Serial(
            port = comPort,
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
        centValue = self.__coinMap.getCentValue(readValue)
        if centValue is None:
            raise ValueError("Cent value " + str(centValue) + " is not valid (raw = " + str(readValue) + ")")
        return centValue

    def shutdown(self):
        self.__serial.close()
        print("Coin acceptor shut down")
