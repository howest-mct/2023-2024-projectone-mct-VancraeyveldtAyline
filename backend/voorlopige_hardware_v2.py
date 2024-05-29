import threading
import time
from RPi import GPIO
from subprocess import check_output
from mcp3008 import MCP3008
from btn_handler import ButtonHandler
from lcd import LCD_Display

# Constant values
BUZZER_PIN = 22
BUTTON_JOY_PIN = 6
LCD_RS_PIN = 21
LCD_E_PIN = 20
LCD_DATA_PINS = [16, 12, 25, 24, 23, 26, 19, 13]
JOYSTICK_CHANNEL_X = 0
JOYSTICK_CHANNEL_Y = 1
LIGHT_CHANNEL = 2
BUTTON_SHUTDOWN = 17

# Initialize objects
mcp3008 = MCP3008()
lcd = LCD_Display(RS=LCD_RS_PIN, E=LCD_E_PIN, data_pins=LCD_DATA_PINS)


# Global variables
joystick_press_count = 0

def callback_btn_joy(pin):
    global joystick_press_count
    joystick_press_count += 1
    print(f"The joystick has been pressed {joystick_press_count} times!")

def long_press_message():
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("Long press!")  # Display long press message
    print('worked2')

def short_press_message():
    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("Short press!")  # Display short press message
    print('worked1')

def setup():
    lcd.send_instruction(0x38)  # Initialize LCD in 8-bit mode, 2 lines, 5x7 characters
    lcd.send_instruction(0x0E)  # Display on, cursor on, blinking on
    lcd.send_instruction(0x01)  # Clear display
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_JOY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_JOY_PIN, GPIO.FALLING, callback=callback_btn_joy, bouncetime=300)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

def get_ip_addresses():
    ips = check_output(['hostname', '--all-ip-addresses']).decode('utf-8').strip().split()
    return ips

def display_ip_addresses():
    ips = get_ip_addresses()

    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("First IP:")  # Send a title to the first line
    lcd.send_instruction(0xC0)  # Move cursor to the second line
    lcd.send_text(ips[0])
    time.sleep(5)

    lcd.send_instruction(0x01)  # Clear display
    lcd.send_instruction(0x80)  # Move cursor to the first line
    lcd.send_text("Second IP:")  # Send a title to the first line
    lcd.send_instruction(0xC0)  # Move cursor to the second line
    lcd.send_text(ips[1])
    time.sleep(5)

def play_tone(buzzer_pin):
    cycles = 5
    for _ in range(cycles):
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.1)

try:
    setup()
    
    ip_thread = threading.Thread(target=display_ip_addresses)
    ip_thread.daemon = True  # Ensure the thread stops when the main program exits
    ip_thread.start()

    button_handler = ButtonHandler(BUTTON_SHUTDOWN, 
                                       long_press_callback=long_press_message,
                                       short_press_duration=1, short_press_callback=short_press_message, long_press_duration=5)
    while True:
        joystick_x_value = mcp3008.read_channel(JOYSTICK_CHANNEL_X)
        joystick_y_value = mcp3008.read_channel(JOYSTICK_CHANNEL_Y)
        light_value = mcp3008.read_channel(LIGHT_CHANNEL)
        # display_ip_addresses()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    mcp3008.close()
    GPIO.cleanup()

