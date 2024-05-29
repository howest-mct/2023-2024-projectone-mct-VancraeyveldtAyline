import threading
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
from RPi import GPIO
from subprocess import check_output
from lcd import LCD_Display
from mcp3008 import MCP3008

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_switch_light')
def switch_light(data):
    print('licht gaat aan/uit', data)



# Constant values
BUZZER_PIN = 22
BUTTON_JOY_PIN = 6
LCD_RS_PIN = 21
LCD_E_PIN = 20
LCD_DATA_PINS = [16, 12, 25, 24, 23, 26, 19, 13]
JOYSTICK_CHANNEL_X = 0
JOYSTICK_CHANNEL_Y = 1
LIGHT_CHANNEL = 2
BUTTON_IPS = 17
BUTTON_SHUTDOWN = 27
CENTER_JOY = 775
THRESHOLD_JOY = 200

# Initialize objects
mcp3008 = MCP3008()
lcd = LCD_Display(RS=LCD_RS_PIN, E=LCD_E_PIN, data_pins=LCD_DATA_PINS)

# Global variables
joystick_press_count = 0
is_add = True

def callback_btn_joy(pin):
    global joystick_press_count
    joystick_press_count += 1
    print(f"The joystick has been pressed {joystick_press_count} times!")

def setup():
    lcd.send_instruction(0x38)  # Initialize LCD in 8-bit mode, 2 lines, 5x7 characters
    lcd.send_instruction(0x0E)  # Display on, cursor on, blinking on
    lcd.send_instruction(0x01)  # Clear display
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_JOY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_JOY_PIN, GPIO.FALLING, callback=callback_btn_joy, bouncetime=300)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_IPS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_IPS, GPIO.FALLING, callback=callback_btn_ips, bouncetime=300)
    GPIO.setup(BUTTON_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_SHUTDOWN, GPIO.FALLING, callback=callback_btn_shut, bouncetime=300)

def get_ip_addresses():
    ips = check_output(['hostname', '--all-ip-addresses']).decode('utf-8').strip().split()
    return ips

# Functie om tekst te tonen
def display_text():
    global is_add
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text(4*(' ')+('+')+(6*' ')+('-')+4*(' '))
    lcd.send_instruction(0xC0)
    if is_add == True:
        lcd.send_text(3*(' ')+'(*)' + 4*' ' + '( )'+3*(' '))
    elif is_add == False:
        lcd.send_text(3*(' ')+'( )' + 4*' ' + '(*)'+3*(' '))


def callback_btn_ips(pin):
    ips = get_ip_addresses()
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("First IP:")  # Send a title to the first line
    lcd.send_instruction(0xC0)  # Move cursor to the second line
    lcd.send_text(ips[0])
    time.sleep(4)  # Wacht 1 seconde
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("Second IP:")  # Send a title to the first line
    lcd.send_instruction(0xC0)  # Move cursor to the second line
    lcd.send_text(ips[1])
    time.sleep(4)
    display_text()

def callback_btn_shut(pin):
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("It's a Shutdown")
    time.sleep(4)  # Wacht 1 seconde
    display_text()



def check_joystick_movement(x_pos):
    """Controleer of de joystick naar links of rechts beweegt."""
    global is_add
    if x_pos < (CENTER_JOY - THRESHOLD_JOY):
        print('Going Left')
        is_add = True
        display_text()
    elif x_pos > (CENTER_JOY + THRESHOLD_JOY):
        print('Going Rigth')
        is_add = False
        display_text()
    else:
        pass


try:
    setup()
    display_text()
    print("**** Starting APP ****")
    socketio.run(app, debug=False, host='0.0.0.0')
    while True:
        joystick_x_value = mcp3008.read_channel(JOYSTICK_CHANNEL_X)
        joystick_y_value = mcp3008.read_channel(JOYSTICK_CHANNEL_Y)
        light_value = mcp3008.read_channel(LIGHT_CHANNEL)
        check_joystick_movement(joystick_x_value)
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()
    mcp3008.close()
