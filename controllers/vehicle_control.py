import serial


class VehicleControl:
    def __init__(self, port):
        self.open(port)

    def reset(self):
        self.set_right(0)
        self.set_left(0)

    def set_right(self, speed):
        self.ser.write(b'r')
        self.ser.write(bytes(str(speed), 'utf8'))

    def set_left(self, speed):
        self.ser.write(b'l')
        self.ser.write(bytes(str(speed), 'utf8'))

    def open(self, port):
        self.ser = serial.Serial(port, 115200)

    def close(self):
        self.ser.close()

    def set_forward(self, vel):
        self.ser.write(b'r')
        self.ser.write(bytes(str(100), 'utf8'))
        self.ser.write(b'l')
        self.ser.write(bytes(str(100), 'utf8'))

    def drive_after_pid(self, steer):
        self.ser.write(b'r')
        self.ser.write(bytes(str(100 + 250 * (1 - steer)), 'utf8'))
        self.ser.write(b'l')
        self.ser.write(bytes(str(100 + 250 * (1 + steer)), 'utf8'))

