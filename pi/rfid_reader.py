import serial

class RfidReader:
    __comPort = '/dev/ttyACM0' # TODO: Configuration value

    def __init__(self):
        self.__serial = serial.Serial(
            port = self.__comPort,
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 0
        )
        self.__serial.flush()
        print("RFID reader connected to serial port " + self.__serial.portstr)

    def readCard(self):
        card = ""
        while card is None or len(card) <= 0:
            # TODO: Support errors from RFID
            # Error code = "E:<error message>"
            card = self.__serial.readline()
        cardNum = int(card) # Only care about the first byte
        return cardNum
