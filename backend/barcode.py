import RPi.GPIO as GPIO
import serial
import time

# Initialize variables
input_string = ""  # Variable to store data from the scanner
data_scanner = ""  # Variable to store data for processing
string_complete = False  # Variable to check if the data has been fully received

# Setup function equivalent
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT)  # Port to trigger the scanner
    global ser
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Initialize serial communication

def loop():
    global input_string, data_scanner, string_complete

    while True:
        GPIO.output(8, GPIO.HIGH)  # Send logic HIGH
        time.sleep(0.2)  # Delay 200 msec
        GPIO.output(8, GPIO.LOW)  # Send logic LOW, simulating a button press to activate the scanner
        time.sleep(0.2)  # Delay 200 msec

        # Check if the data from the scanner has been fully received
        if string_complete:
            if data_scanner == "8859411300023\r\n":  # If the data matches, print "OK"
                print("OK")
                time.sleep(1)
            else:
                print("No Data")  # If the data doesn't match, print "No Data"

            # Clear the variables for new data
            input_string = ""
            data_scanner = ""
            string_complete = False

def serial_event():
    global input_string, data_scanner, string_complete

    while ser.in_waiting:
        in_char = ser.read().decode('utf-8')
        input_string += in_char
        if in_char == '\n':  # If newline character is received, set the flag
            string_complete = True
            data_scanner = input_string

if __name__ == "__main__":
    setup()
    try:
        while True:
            loop()
            serial_event()
    except KeyboardInterrupt:
        GPIO.cleanup()
