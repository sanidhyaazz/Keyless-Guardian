import serial
import serial.tools.list_ports
from attendance_markup import make_attendance

def find_serial_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:  # Adjust for your device
            return port.device  # Returns something like '/dev/ttyUSB0' (Linux) or 'COM3' (Windows)
    return None

# Automatically set the port
use = find_serial_port()

if use is None:
    print("No suitable serial device found.")
    exit(1)  # Exit if no port is found

print(f"Using serial port: {use}")

serialPort = serial.Serial(port=use, baudrate=115200, timeout=0.1)
serialPort.flush()

while True:
    if serialPort.in_waiting > 0:  # Check if data is not empty
        decoded_data = serialPort.readline().decode('utf-8').strip()
        decoded_data = decoded_data.split()
        
        # Extract UID from the data
        for i in range(len(decoded_data)):
            if decoded_data[i] == 'UID:':
                uid = decoded_data[i + 1]
                print(uid)
                result = make_attendance(uid)
                print(result)
                
                # Check if UID is authorized
                if result == "0":
                    print("Unauthorized UID ")
                    print("UID: ", uid)
                    serialPort.write(b" False\n")
                elif result == "Error":
                    print("Server Error")
                    serialPort.write(b" Error\n")
                else:
                    print("Access Granted! ")
                    print("UID: ", uid)
                    result = " "+ result
                    serialPort.write(result.encode(encoding="utf-8"))