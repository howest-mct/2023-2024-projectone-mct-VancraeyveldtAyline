from RPi import GPIO
import time
from lcd import LCD_Display

LCD_RS_PIN = 21
LCD_E_PIN = 20
LCD_DATA_PINS = [16, 12, 25, 24, 23, 26, 19, 13]
BUTTON_SHUTDOWN = 17



try:
    lcd = LCD_Display(RS=LCD_RS_PIN, E=LCD_E_PIN, data_pins=LCD_DATA_PINS, )
    GPIO.setup(BUTTON_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Button pin
    lcd.display_default_message()
    
    while True:
        button_state = GPIO.input(BUTTON_SHUTDOWN)
        if button_state == GPIO.HIGH:
            time.sleep(0.05) # Debouncing delay
            if GPIO.input(BUTTON_SHUTDOWN) == GPIO.HIGH:
                start_time = time.time()
                while GPIO.input(BUTTON_SHUTDOWN) == GPIO.HIGH:
                    time.sleep(0.1)
                duration = (time.time() - start_time) * 1000 # Convert to milliseconds
                lcd.display_button_press_duration(duration)
                time.sleep(2)
                lcd.display_default_message()
        else:
            lcd.display_default_message()
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()