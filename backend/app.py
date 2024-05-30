import threading
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
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

@app.route('/historiek/', methods=['GET'])
def get__historiek():
    if request.method == 'GET':
        complete_historiek = DataRepository.read_records_historiek()
        if complete_historiek is not None:
            return jsonify(historiek=complete_historiek), 200
        else:
            return jsonify(message="error"), 404

@app.route('/historiek/<deviceid>/', methods=['GET'])
def get_records_device(deviceid):
    if request.method == 'GET':
        records = DataRepository.read_records_historiek_by_id(deviceid)
        if records is not None:
            return jsonify(trein=records), 200
        else:
            return jsonify(message='error'), 404

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')


# *************** HARDWARE ***************


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
THRESHOLD_LIGHT = 700

# Initialize objects
mcp3008 = MCP3008()
lcd = LCD_Display(RS=LCD_RS_PIN, E=LCD_E_PIN, data_pins=LCD_DATA_PINS)

# Global variables
joystick_press_count = 0
is_add = True
is_open = False

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

def check_joystick_hor_movement(x_pos):
    global is_add
    if x_pos < (CENTER_JOY - THRESHOLD_JOY):
        print('Going Left')
        is_add = True
        display_text()
        DataRepository.insert_values_historiek(3, x_pos, 'x-pos: left')
    elif x_pos > (CENTER_JOY + THRESHOLD_JOY):
        print('Going Rigth')
        is_add = False
        display_text()
        DataRepository.insert_values_historiek(3, x_pos, 'x-pos: rigth')
    else:
        pass

def check_joystick_ver_movement(y_pos):
    global is_add
    if y_pos < (CENTER_JOY - THRESHOLD_JOY):
        print('Going Up')
        DataRepository.insert_values_historiek(3, y_pos, 'y_pos: up')
    elif y_pos > (CENTER_JOY + THRESHOLD_JOY):
        print('Going Down')
        DataRepository.insert_values_historiek(3, y_pos, 'y_pos: down')
    else:
        pass

def check_lightsensor_activity(light_value):
    global is_open
    if light_value < THRESHOLD_LIGHT:
        if is_open == False:
            print("Kast is geopend")
            is_open = True
            DataRepository.insert_values_historiek(1, light_value, 'opened')
    elif light_value >= THRESHOLD_LIGHT:
        if is_open == True:
            print("Kast is gesloten")
            is_open = False
            DataRepository.insert_values_historiek(1, light_value, 'closed')

def main_loop():
    while True:
        joystick_x_value = mcp3008.read_channel(JOYSTICK_CHANNEL_X)
        joystick_y_value = mcp3008.read_channel(JOYSTICK_CHANNEL_Y)
        light_value = mcp3008.read_channel(LIGHT_CHANNEL)
        check_joystick_hor_movement(joystick_x_value)
        check_joystick_ver_movement(joystick_y_value)
        check_lightsensor_activity(light_value)
        time.sleep(1)

def run_flask():
    socketio.run(app, debug=False, host='0.0.0.0')

try:
    setup()
    display_text()
    print("**** Starting APP ****")
    flask_thread = threading.Thread(target=run_flask)
    main_thread = threading.Thread(target=main_loop)
    flask_thread.start()
    main_thread.start()
    flask_thread.join()
    main_thread.join()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()
    mcp3008.close()