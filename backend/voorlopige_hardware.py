import time
from RPi import GPIO

# Klassen
from mcp3008 import MCP3008
mcp3008 = MCP3008()


def setup():
    GPIO.setmode(GPIO.BCM)

try:
        setup()
        while True:
            value0 = mcp3008.read_channel(0)
            value1 = mcp3008.read_channel(1)
            value2 = mcp3008.read_channel(2)
            print("Waarde op kanaal 0: {}".format(value0))
            print("Waarde op kanaal 1: {}".format(value1))
            print("Waarde op kanaal 2: {}".format(value2))
            time.sleep(1) 
except KeyboardInterrupt:
    mcp3008.close()
    GPIO.cleanup()