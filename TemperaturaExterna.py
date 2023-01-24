import smbus2
import bme280

class TemperaturaExterna:
    def __init__(self):
        self.port = 1
        self.address = 0x76
        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)
    
    def atualizar_temperatura(self):
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)
        return self.data.temperature
