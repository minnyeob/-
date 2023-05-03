import serial
import time

signal = serial.Serial('COM6', 9600)

def read_from_arduino():
    while signal.inWaiting() == 0:
        pass
    return signal.readline().decode().strip()

def write_to_arduino(data):
    signal.write(data.encode())

def control_led(state):
    if state:
        write_to_arduino('1')
    else:
        write_to_arduino('0')

def main():
    try:
        print(read_from_arduino())

        control_led(True)
        time.sleep(2)

        
        control_led(False)
        time.sleep(2)
    
    except KeyboardInterrupt:
        print('program off')

    finally:
        signal.close()

if __name__ == '__main__':
    main()