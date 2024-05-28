import time
from RPi import GPIO

from mcp3008 import MCP3008
mcp3008 = MCP3008()
from btn_handler import ButtonHandler
button_handler = ButtonHandler(18)
from lcd import LCD_Display
from subprocess import check_output
lcd = LCD_Display(RS=21, E=20, data_pins=[16, 12, 25, 24, 23, 26, 19, 13])


buzzer = 22
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
    GPIO.setup(buzzer, GPIO.OUT)

def play_tone(buzzer):
    cycles = 5
    
    for _ in range(cycles):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(0.1)

def get_ip_address():
    ips = check_output(['hostname', '--all-ip-addresses'])
    ip_address = ""
    for byte in ips:
        ip_address += chr(byte)
    return ip_address


try:
        setup()
        while True:
            waarde_joyx = mcp3008.read_channel(0)
            waarde_joyy = mcp3008.read_channel(1)
            waarde_licht = mcp3008.read_channel(2)
            print(get_ip_address)
            lcd.send_text(get_ip_address())
            play_tone(buzzer)
            time.sleep(1) 
except KeyboardInterrupt:
    mcp3008.close()
    GPIO.cleanup()