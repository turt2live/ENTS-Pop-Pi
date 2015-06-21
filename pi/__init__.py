import RPi.GPIO as GPIO
from time import sleep
from main import PopPi

app = None
try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    app = PopPi()
    app.start()

    while True:
        sleep(0.1)
        continue
except KeyboardInterrupt:
    if not app is None:
        app.stop()
    GPIO.cleanup()
