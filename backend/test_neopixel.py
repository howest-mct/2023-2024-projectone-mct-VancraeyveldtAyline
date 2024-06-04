import time
from rpi_ws281x import PixelStrip, Color
# LED strip configuratie:
LED_COUNT = 24       # Aantal LED pixels.
LED_PIN = 18         # GPIO pin verbonden met de pixels (moet overeenkomen met de gekozen pin).
LED_FREQ_HZ = 800000 # LED signaal frequentie in hertz (meestal 800kHz)
LED_DMA = 10         # DMA kanaal om aan te sturen (moet 10 zijn)
LED_BRIGHTNESS = 255 # Helderheid van de LED's (0-255)
LED_INVERT = False   # Invert het signaal (True of False)
LED_CHANNEL = 0      # Kanaal (moet 0 of 1 zijn)

# Initialiseer de LED strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

try:
    print('Druk op Ctrl-C om te stoppen')
    while True:
        colorWipe(strip, Color(0, 0, 255))
        time.sleep(1)
        colorWipe(strip, Color(0, 255, 0))
        time.sleep(1)
        # Draai een rode kleur door de LED's
        colorWipe(strip, Color(255, 0, 0))
        time.sleep(1)

except KeyboardInterrupt:
    # Clear de LED strip bij het afsluiten
    colorWipe(strip, Color(0, 0, 0), 10)