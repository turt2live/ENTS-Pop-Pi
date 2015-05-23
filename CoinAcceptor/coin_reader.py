import serial, time

class CoinAcceptor:
    # Reads from the sparkfun 6-coin acceptor
    # (sparkfun part COM-11636, model DG600F(S))

    __comPort = '/dev/ttyAMA0' # TODO: Configuration variable

    def __init__(self):
        self.__serial = serial.Serial(
            port = self.__comPort,
            baudrate = 9600,
            parity = serial.PARITY_EVEN,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 0
        )
        print("Connected to serial port " + self.__serial.portstr)

    def inhibit(self, inhibited):
        # TODO: Actually do inhibiting
        if !inhibited:
            # Clear buffer if we're clearing our inhibit state
            self.__serial.flush()
        return

    def readCoin(self):
        coin = ""
        while coin is not None and len(coin) > 0:
            coin = self.__serial.read()
        ch = ord(coin[0]) # Only care about first character (byte)
        centValue = -1
        if ch == 0x0A:
            centValue = 25
        elif ch == 0x14:
            centValue = 100
        elif ch == 0x1E:
            centValue = 200
        if centValue < 0:
            raise ValueError("Cent value " + centValue + " is not valid")
        return centValue
