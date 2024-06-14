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

def send_qr_code(data_string):
    try:
        byte_string = data_string.encode('utf-8')
        ser.write(byte_string)
        print(f"Sent: {byte_string}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    # De string die je wilt versturen als QR-code
    qr_code_string = 00910001

    # Verstuur de QR-code naar de barcode scanner
    send_qr_code(qr_code_string)

    # Begin met het lezen van gegevens van de seriële poort
    read_from_serial()
