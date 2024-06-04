from RPi import GPIO
import time

class LCD_Display:
    # Eerste de laagste bit gebruiken
    def __init__(self, RS, E, data_pins):
        self.RS = RS
        self.E = E
        self.data_pins = data_pins
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)
        for pin in self.data_pins:
            GPIO.setup(pin, GPIO.OUT)

    def send_instruction(self, instruction):
        GPIO.output(self.RS, GPIO.LOW)
        GPIO.output(self.E, GPIO.HIGH)
        for i in range(8):
            GPIO.output(self.data_pins[i], instruction >> i & 0x01)
        time.sleep(0.001)
        GPIO.output(self.E, GPIO.LOW)

    def send_character(self, character):
        GPIO.output(self.RS, GPIO.HIGH)
        GPIO.output(self.E, GPIO.HIGH)
        for i in range(8):
            GPIO.output(self.data_pins[i], character >> i & 0x01)
        time.sleep(0.001)
        GPIO.output(self.E, GPIO.LOW)

    def send_text(self, text):
        line_length = 16
        current_line = 0

        for char in text:
            if char == '\n' or current_line >= line_length:
                if char == '\n':
                    self.send_instruction(0xC0)
                else:
                    self.send_instruction(0xC0) if current_line >= line_length else self.send_instruction(0x80)
                current_line = 0
            else:
                current_line += 1

            self.send_character(ord(char))

    def scroll_text(self, text, line=0, delay=0.5):
        if line == 1:
            self.send_instruction(0xC0)
        else:
            self.send_instruction(0x80)

        display_text = text.ljust(16)
        for i in range(len(display_text)):
            self.send_text(display_text[i:i+16])
            time.sleep(delay)
            if line == 1:
                self.send_instruction(0xC0)
            else:
                self.send_instruction(0x80)
