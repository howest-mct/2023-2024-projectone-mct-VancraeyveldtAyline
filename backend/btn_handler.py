import RPi.GPIO as GPIO
import time
import threading

class ButtonHandler:
    def __init__(self, pin):
        self.pin = pin
        self.is_pressed = False
        self.press_time = 0
        self.long_press_duration = 5
        self.message_sent = False
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.button_event)

    def button_event(self, channel):
        if GPIO.input(self.pin) == GPIO.LOW:
            self.press_button()
        else:
            self.release_button()

    def press_button(self):
        self.is_pressed = True
        self.press_time = time.time()
        self.message_sent = False
        threading.Thread(target=self.check_long_press).start()

    def release_button(self):
        self.is_pressed = False

    def check_long_press(self):
        while self.is_pressed:
            current_time = time.time()
            if current_time - self.press_time >= self.long_press_duration and not self.message_sent:
                self.send_message()
                self.message_sent = True

    def send_message(self):
        print("Knop was lang genoeg ingedrukt!")
        # Hier kun je de code toevoegen om een bericht te sturen


