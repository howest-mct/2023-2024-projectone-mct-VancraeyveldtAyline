import RPi.GPIO as GPIO
import time
import threading

class ButtonHandler:
    def __init__(self, pin, long_press_duration=5, long_press_callback=None, short_press_duration=1, short_press_callback=None):
        self.pin = pin
        self.long_press_duration = long_press_duration
        self.long_press_callback = long_press_callback
        self.short_press_duration = short_press_duration
        self.short_press_callback = short_press_callback
        self.is_pressed = False
        self.press_time = 0
        self.long_press_thread = None
        self.stop_event = threading.Event()
        
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
        self.stop_event.clear()
        self.long_press_thread = threading.Thread(target=self.check_long_press)
        self.long_press_thread.start()

    def release_button(self):
        self.is_pressed = False
        self.stop_event.set()  # Signal the thread to stop
        if self.long_press_thread is not None:
            self.long_press_thread.join()  # Wait for the thread to finish

    def check_long_press(self):
        while not self.stop_event.is_set():
            current_time = time.time()
            if current_time - self.press_time >= self.long_press_duration:
                if self.long_press_callback:
                    self.long_press_callback(self.pin)  # Call the long press callback function
                break
            elif current_time - self.press_time >= self.short_press_duration and not self.is_pressed:
                if self.short_press_callback:
                    self.short_press_callback(self.pin)  # Call the short press callback function
                break
            time.sleep(0.1)  # Add a small delay to reduce CPU usage

