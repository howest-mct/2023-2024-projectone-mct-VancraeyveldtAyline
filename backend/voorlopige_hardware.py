import time
from RPi import GPIO

# Klassen
from mcp3008 import MCP3008
mcp3008 = MCP3008()
from btn_handler import ButtonHandler
button_handler = ButtonHandler(18)

btn_joy = 6
aantal_joystick_ingedrukt = 0

def callback_btn_joy(pin):
    global aantal_joystick_ingedrukt, current_status
    aantal_joystick_ingedrukt += 1
    print("Er is {} keer op de joystick gedrukt!".format(aantal_joystick_ingedrukt))

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn_joy, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn_joy, GPIO.FALLING, callback=callback_btn_joy, bouncetime=300)

try:
        setup()
        while True:
            waarde_joyx = mcp3008.read_channel(0)
            waarde_joyy = mcp3008.read_channel(1)
            waarde_licht = mcp3008.read_channel(2)
            # print("Waarde op kanaal 0: {}".format(waarde_joyx))
            # print("Waarde op kanaal 1: {}".format(waarde_joyy))
            # print("Waarde op kanaal 2: {}".format(waarde_licht))
            time.sleep(1) 
except KeyboardInterrupt:
    mcp3008.close()
    GPIO.cleanup()