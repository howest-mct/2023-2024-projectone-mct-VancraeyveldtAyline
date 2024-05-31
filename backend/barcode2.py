import serial
import time

# Stel de seriële poort in
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Gebruik /dev/ttyS0 voor oudere RPi-modellen
    baudrate=9600,
    timeout=1
)

def read_from_serial():
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline()
                print(f"Received: {line.decode()}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        ser.close()

if __name__ == "__main__":
    read_from_serial()





# byte_string = b'\x00\x00\x00\xf4\x1e8\xf8\xc0H\x92\x1c\xdf\x08V\x0f\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x00@ \x00\xb1\xfc\xfd\x9e\x00\x00\x90\x00\x00\x00>\x00\x01 \x83\xfc\x1f\x00\xe0\x80p\x00\xe3\x00\xe0\x00\xf8\x00\x06\x10\xe0\x01\x00\x00\x00\x000\xa0\x00\x05\x00\x00\x13@\x88\x02@\x00\x00 +\x00\x03\x04\x00\x80\xd0\x00\x05\x022\x00\xc1{\x03\x01\x00\x00\x00\x00\xfb\x00\x00\xc8\x00\x80\xbeB\xde\xf8\xe0\xe0\x01\x00#\xff; \x00\xf8\x80\xfc\x02\x05\x00\xbf\x00\xf8\xfe\xfc\x00!\x00\x00\x00\x02'

# # Decodeer de bytestring naar een string
# decoded_string = byte_string.decode('utf-8')

# # Print de gedecodeerde string
# print(f"Decoded string: '{decoded_string}'")
# print(f"Length of decoded string: {len(decoded_string)}")
