import serial
import time


ser = serial.Serial(
    port='/dev/ttyUSB0', 
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

