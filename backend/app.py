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
from rpi_ws281x import PixelStrip, Color
import serial
from datetime import datetime
import os


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


# ****************** PRODUCTS ****************** 
@app.route('/inventory/', methods=['GET'])
def get_inventory():
    if request.method == 'GET':
        inventory = DataRepository.read_products()
        if inventory is not None:
            return jsonify(inventory=inventory), 200
        else:
            return jsonify(message="error"), 404

@app.route('/product-history/', methods=['GET'])
def get_product_history():
    if request.method == 'GET':
        history = DataRepository.read_records_product_historiek()
        if history is not None:
            return jsonify(history=history), 200
        else:
            return jsonify(message="error"), 404

@app.route('/cart/', methods=['GET'])
def get_products_under():
    if request.method == 'GET':
        cart = DataRepository.read_products_under()
        if cart is not None:
            return jsonify(cart=cart), 200
        else:
            return jsonify(message="error"), 404

# ****************** HISTORIEK ******************   
@app.route('/historiek/', methods=['GET'])
def get_historiek():
    if request.method == 'GET':
        complete_historiek = DataRepository.read_records_historiek()
        if complete_historiek is not None:
            return jsonify(historiek=complete_historiek), 200
        else:
            return jsonify(message="error"), 404

@app.route('/historiek/<filter>/', methods=['GET'])
def get_records_device(filter):
    if request.method == 'GET':
        records = DataRepository.read_records_historiek_by_id(filter)
        if records is not None:
            return jsonify(history=records), 200
        else:
            return jsonify(message='error'), 404


# ****************** TYPES ******************
@app.route('/types/', methods=['GET', 'POST'])
def get_types():
    if request.method == 'GET':
        types = DataRepository.read_types()
        if types is not None:
            return jsonify(types=types), 200
        else:
            return jsonify(message="error"), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        DataRepository.create_type()
        data = DataRepository.create_type(gegevens['product_type'])
        return jsonify(typeid = data), 201

@app.route('/types/<typeid>/', methods=['GET', 'DELETE', 'PUT'])
def get_type_by_id(typeid):
    if request.method == 'GET':
        producttype = DataRepository.read_type(typeid)
        if producttype is not None:
            return jsonify(type=producttype), 200
        else:
            return jsonify(message='error'), 404
    elif request.method == 'DELETE':
        data = DataRepository.delete_type(typeid)
        return jsonify(status = data), 200
    elif request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)
        data = DataRepository.update_type(typeid, gegevens['product_type'])
        if data is not None:
            if data > 0:
                return jsonify(typeid = id), 200
            else:
                return jsonify(status=data), 200
        else:
            return jsonify(message="error"), 404


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    global is_buzzer
    if is_buzzer == 1:
        socketio.emit('B2F_set_switch', {'status': True})
    elif is_buzzer == 0:
        socketio.emit('B2F_set_switch', {'status': False})
    first_check_door()
    socketio.emit('B2F_lighting', {'color': lighting_color})
    print('A new client connect')

@socketio.on("F2B_shutdown")
def shutdown(status):
    if status.status == 1:
        os.system("sudo poweroff")


@socketio.on("F2B_buzzer")
def change_buzzer(status):
    global is_buzzer
    is_buzzer = status['status']
    DataRepository.update_voorkeur(4, 1, "buzzer_status", status['status'])

@socketio.on("F2B_lighting")
def change_color(color):
    global lighting_color
    lighting_color = color['color']
    if lighting_color == 'green':
        DataRepository.update_voorkeur(5, 1, "lighting_color", 1)
    if lighting_color == 'blue':
        DataRepository.update_voorkeur(5, 1, "lighting_color", 2)
    if lighting_color == 'red':
        DataRepository.update_voorkeur(5, 1, "lighting_color", 3)



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
THRESHOLD_LIGHT = 400
MIN_NUMBER_LCD = -20
MAX_NUMBER_LCD = 20


# LED strip configuratie:
LED_COUNT = 24       # Aantal LED pixels.
LED_PIN = 18         # GPIO pin verbonden met de pixels (moet overeenkomen met de gekozen pin).
LED_FREQ_HZ = 800000 # LED signaal frequentie in hertz (meestal 800kHz)
LED_DMA = 10         # DMA kanaal om aan te sturen (moet 10 zijn)
LED_BRIGHTNESS = 255 # Helderheid van de LED's (0-255)
LED_INVERT = False   # Invert het signaal (True of False)
LED_CHANNEL = 0      # Kanaal (moet 0 of 1 zijn)

# Initialize objects
mcp3008 = MCP3008()
lcd = LCD_Display(RS=LCD_RS_PIN, E=LCD_E_PIN, data_pins=LCD_DATA_PINS)
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=1
)

# Global variables
is_buzzer = (DataRepository.read_voorkeur_by_description("buzzer_status"))["voorkeur_waarde"]
is_add = True
is_open = False
is_neolight = False
is_barcode = False
current_number = 1
barcode = ''
required_press_time = 3
press_start_time = None

lighting_color_value = (DataRepository.read_voorkeur_by_description("lighting_color"))["voorkeur_waarde"]
if lighting_color_value == 1:
    lighting_color = "green"
if lighting_color_value == 2:
    lighting_color = "blue"
if lighting_color_value == 3:
    lighting_color = "red"

def callback_btn_joy(pin):
    global is_barcode, current_number, barcode, is_buzzer, is_neolight
    if is_barcode == True:
        DataRepository.insert_values_product_historiek(current_number, barcode)
        lcd.send_instruction(0x01)  # Clear display
        lcd.send_instruction(0x80)
        lcd.send_text("Succes!")
        if is_buzzer == 1:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(1)
        product = DataRepository.read_product_historiek_by_barcode(barcode)
        formatted_date = product["tijdstip"].strftime('%Y-%m-%d %H:%M:%S')
        socketio.emit("B2F_product_change", {"name": product["product_naam"], "category":product["product_type"], "date":formatted_date, "change":product["product_aantal_wijziging"]})
        is_barcode = False
        is_neolight = True
        display_text()

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

def get_ip_addresses():
    ips = check_output(['hostname', '--all-ip-addresses']).decode('utf-8').strip().split()
    return ips

def display_text():
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("Welcome back!")

def callback_btn_ips(pin):
    ips = get_ip_addresses()
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("First IP:")  # Send a title to the first line
    lcd.send_instruction(0xC0)  # Move cursor to the second line
    lcd.send_text(ips[0])
    time.sleep(4)
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("Second IP:")  # Send a title to the first line
    lcd.send_instruction(0xC0)  # Move cursor to the second line
    lcd.send_text(ips[1])
    time.sleep(4)
    display_text()

def check_button():
    global press_start_time
    while True:
        if GPIO.input(BUTTON_SHUTDOWN) == GPIO.LOW: 
            if press_start_time is None:
                press_start_time = time.time()
            elif time.time() - press_start_time >= required_press_time:
                lcd.send_instruction(0x01) 
                lcd.send_instruction(0x80)
                lcd.send_text("It's a Shutdown")
                os.system("sudo poweroff")
                press_start_time = None 
        else: 
            press_start_time = None
        time.sleep(0.1)  

def check_joystick_movement(x_pos, y_pos):
    global is_neolight, current_number, is_barcode
    if abs(x_pos - CENTER_JOY) > abs(y_pos - CENTER_JOY):
        if (x_pos < (CENTER_JOY - THRESHOLD_JOY)):
            DataRepository.insert_values_historiek(3, x_pos, 'x-pos: left')
            socketio.emit("B2F_xpos_left", {"sensor": 3, "pos": x_pos, "message": 'x-pos: left'})
            record = DataRepository.read_latest_record_historiek_by_id(3)
            formatted_date = record["tijdstip_waarde"].strftime('%Y-%m-%d %H:%M:%S')
            socketio.emit("B2F_joystick", {"value": record["waarde"], "date":formatted_date, "note":record["opmerking"]})
        elif (x_pos > (CENTER_JOY + THRESHOLD_JOY)):
            DataRepository.insert_values_historiek(3, x_pos, 'x-pos: right')
            socketio.emit("B2F_xpos_right", {"sensor": 3, "pos": x_pos, "message": 'x-pos: right'})
            record = DataRepository.read_latest_record_historiek_by_id(3)
            formatted_date = record["tijdstip_waarde"].strftime('%Y-%m-%d %H:%M:%S')
            socketio.emit("B2F_joystick", {"value": record["waarde"], "date":formatted_date, "note":record["opmerking"]})
    else:
        while is_barcode == True:
            x_pos = mcp3008.read_channel(JOYSTICK_CHANNEL_X)
            y_pos = mcp3008.read_channel(JOYSTICK_CHANNEL_Y)
            if (y_pos < (CENTER_JOY - THRESHOLD_JOY)):
                if current_number < MAX_NUMBER_LCD:
                    current_number += 1
                    display_number(current_number)
                    time.sleep(0.2)
                DataRepository.insert_values_historiek(3, y_pos, 'y_pos: up')
                socketio.emit("B2F_ypos_up", {"sensor": 3, "pos": y_pos, "message": 'y-pos: up'})
                record = DataRepository.read_latest_record_historiek_by_id(3)
                formatted_date = record["tijdstip_waarde"].strftime('%Y-%m-%d %H:%M:%S')
                socketio.emit("B2F_joystick", {"value": record["waarde"], "date":formatted_date, "note":record["opmerking"]})
            elif (y_pos > (CENTER_JOY + THRESHOLD_JOY)):
                if current_number > MIN_NUMBER_LCD:
                    current_number -= 1
                    display_number(current_number)
                    time.sleep(0.2)
                DataRepository.insert_values_historiek(3, y_pos, 'y_pos: down')
                socketio.emit("B2F_ypos_down", {"sensor": 3, "pos": y_pos, "message": 'y-pos: down'})
                record = DataRepository.read_latest_record_historiek_by_id(3)
                formatted_date = record["tijdstip_waarde"].strftime('%Y-%m-%d %H:%M:%S')
                socketio.emit("B2F_joystick", {"value": record["waarde"], "date":formatted_date, "note":record["opmerking"]})

def check_lightsensor_activity(light_value):
    global is_open
    if light_value < THRESHOLD_LIGHT:
        if is_open == False:
            is_open = True  
            DataRepository.insert_values_historiek(1, light_value, 'opened')
            socketio.emit("B2F_light_open", {"sensor": 1, "value": light_value, "message": 'opened'})
            record = DataRepository.read_latest_record_historiek_by_id(1)
            formatted_date = record["tijdstip_waarde"].strftime('%Y-%m-%d %H:%M:%S')
            socketio.emit("B2F_light", {"value": record["waarde"], "date":formatted_date, "note":record["opmerking"]})

    elif light_value >= THRESHOLD_LIGHT:
        if is_open == True:
            is_open = False
            DataRepository.insert_values_historiek(1, light_value, 'closed')
            socketio.emit("B2F_light_close", {"sensor": 1, "value": light_value, "message": 'closed'})
            record = DataRepository.read_latest_record_historiek_by_id(1)
            formatted_date = record["tijdstip_waarde"].strftime('%Y-%m-%d %H:%M:%S')
            socketio.emit("B2F_light", {"value": record["waarde"], "date":formatted_date, "note":record["opmerking"]})

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def set_color(strip, color):
    if color == "none":
        color_value = Color(0,0,0)
    if color == "green":
        color_value = Color(0,255,0)
    if color == "red":
        color_value = Color(255,0,0)
    if color == "blue":
        color_value = Color(0,0,255)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color_value)
    strip.show()

def neopixelring():
    global is_neolight
    if is_neolight == True:
        set_color(strip, lighting_color)
        time.sleep(0.5)
        set_color(strip, "none")
        is_neolight = False

def display_number(number):
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text(f"Amount: {number}")

def read_barcode():
    global current_number, is_barcode, barcode
    if ser.in_waiting > 0:
        line = ser.readline()
        barcode = line.decode().rstrip()
        DataRepository.insert_values_historiek(2, barcode, "barcode gescant")
        lcd.send_instruction(0x01)  # Clear display
        lcd.send_instruction(0x80)  # Move cursor to the first line

        record = DataRepository.read_latest_record_historiek_by_id(2)
        formatted_date = record["tijdstip_waarde"].strftime('%Y-%m-%d %H:%M:%S')
        socketio.emit("B2F_barcode", {"value": record["waarde"], "date":formatted_date, "note":record["opmerking"]})

        if DataRepository.read_product_name_by_barcode(barcode) == None:
            lcd.send_text('not found')
            time.sleep(3)
            display_text()
        else:
            is_barcode = True
            product_name_object = DataRepository.read_product_name_by_barcode(barcode)
            product_name = product_name_object['product_naam']
            lcd.send_text(product_name)
            time.sleep(3)
            lcd.send_instruction(0xC0)
            current_number = 1
            display_number(current_number)
    time.sleep(0.1)
        
def run_flask():
    socketio.run(app, debug=False, host='0.0.0.0')

def main_loop():
    while True:
        joystick_x_value = mcp3008.read_channel(JOYSTICK_CHANNEL_X)
        joystick_y_value = mcp3008.read_channel(JOYSTICK_CHANNEL_Y)
        light_value = mcp3008.read_channel(LIGHT_CHANNEL)
        check_joystick_movement(joystick_x_value, joystick_y_value)
        check_lightsensor_activity(light_value)
        neopixelring() 
        read_barcode()
        time.sleep(1)

def first_check_door():
    global is_open
    light_value = mcp3008.read_channel(LIGHT_CHANNEL)
    if light_value < THRESHOLD_LIGHT:
        is_open = True
        socketio.emit("B2F_light_open", {"sensor": 1, "value": light_value, "message": 'first check'})
    elif light_value >= THRESHOLD_LIGHT:
        is_open = False
        socketio.emit("B2F_light_close", {"sensor": 1, "value": light_value, "message": 'first check'})

try:
    is_neolight = True
    setup()
    display_text()
    print("**** Starting APP ****")
    button_thread = threading.Thread(target=check_button)
    flask_thread = threading.Thread(target=run_flask)
    main_thread = threading.Thread(target=main_loop)
    button_thread.daemon = True
    button_thread.start()
    flask_thread.start()
    main_thread.start()
    flask_thread.join()
    main_thread.join()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()
    # Zorg ervoor dat je ser en mcp3008 alleen sluit als ze bestaan
    try:
        ser.close()
    except NameError:
        pass
    try:
        mcp3008.close()
    except NameError:
        pass
