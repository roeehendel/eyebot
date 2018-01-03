import serial

class ForceClass:
    def __init__(self, port):
        self.port = port
        self.open()

    def read_details(self):
        self.ser.write(b'r')
        force = int(self.ser.readline())
        return force

    def open(self):
        self.ser = serial.Serial(self.port, 9600)

    def close(self):
        self.ser.close()

    def reset(self):
        self.close()
        self.open()
