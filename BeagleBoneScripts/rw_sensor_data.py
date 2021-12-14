import serial


def append_csv(filepath, byte_string):
    row=byte_string.decode('utf-8')
    with open(filepath, 'a', newline='\n') as f:
        f.write(row)

serialPort = serial.Serial(
    port='COM3')

eol = b'\r'
filepath = 'sensor_data.csv'

while(1):
    with serialPort as ser:
        x = ser.read_until(eol)
        print(x)
        append_csv(filepath, x)
