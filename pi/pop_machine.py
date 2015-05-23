import RPi.GPIO as GPIO
from time import sleep

class PopMachine:
    # Manipulates the pop machine interface. Should be designed
    # to mask implementation details.

    __relayPin = 18 # TODO: Configuration value

    def __init__(self):
        GPIO.setup(self.__relayPin, GPIO.OUT)
        GPIO.output(self.__relayPin, GPIO.LOW)

    def getPopCost(self):
        return 100 # TODO: Expand this somehow to support per-pop prices?

    def awardPop(self):
        # TODO: Expand this to somehow support per-pop prices?
        # This code was copied from the old master branch
        sleep(1)
        GPIO.output(self.__relayPin, GPIO.LOW)
        sleep(1)
        GPIO.output(self.__relayPin, GPIO.HIGH)
        sleep(1)
        GPIO.output(self.__relayPin, GPIO.LOW)

    def shutdown(self):
        return # Nothing to do
