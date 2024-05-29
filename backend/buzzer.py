import RPi.GPIO as GPIO
import time

# Definieer de pin voor de buzzer
BUZZER_PIN = 22

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

def play_tone(pin, frequency, duration):
    """Speel een toon af met een bepaalde frequentie en duur."""
    period = 1.0 / frequency
    cycles = int(frequency * duration)
    for i in range(cycles):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(period / 2)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(period / 2)

def no_tone(pin):
    """Stop het afspelen van een toon."""
    GPIO.output(pin, GPIO.LOW)

def loop():
    # Voorbeeldtoon: 440 Hz (A4) voor 1 seconde
    play_tone(BUZZER_PIN, 440, 1)
    time.sleep(1)
    no_tone(BUZZER_PIN)

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        no_tone(BUZZER_PIN)
        GPIO.cleanup()
