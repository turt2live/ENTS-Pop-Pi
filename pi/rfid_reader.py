import serial

class RfidReader:
    # Reads RFId from an Arduino (ideally).
    # Protocol:
    # - Linefeed indicates end of message
    # - If message starts with 'E:' then the following characters
    #   indicate the error that occurred.
    # - If the message does not start with 'E:' then the message is
    #   assumed as numeric and therefore a fob/card number.

    def __init__(self, comPort):
        self.__serial = serial.Serial(
            port = comPort,
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = None # Wait forever
        )
        self.__serial.flush()
        print("RFID reader connected to serial port " + self.__serial.portstr)

    def readCard(self):
        self.__serial.flush()
        card = ""
        while card is None or len(card) <= 0:
            # TODO: Support errors from RFID
            # Error code = "E:<error message>"
            card = self.__serial.readline()
        cardNum = int(card)
        return cardNum

    def shutdown(self):
        self.__serial.close()
        print("RFID reader shut down")
