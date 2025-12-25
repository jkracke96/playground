from gpiozero import OutputDevice
from spidev import SpiDev


class Relay:
    """Lightweight wrapper around gpiozero.OutputDevice.

    Using composition instead of subclassing avoids accidental signature
    mismatches with gpiozero's internal classes on different platforms.
    """
    def __init__(self, pin, active_high=False, initial_value=False, pin_factory=None):
        self.device = OutputDevice(pin, active_high=active_high,
                                   initial_value=initial_value,
                                   pin_factory=pin_factory)

    def on(self):
        return self.device.on()

    def off(self):
        return self.device.off()

    def close(self):
        return self.device.close()

    @property
    def is_active(self):
        return self.device.is_active
    
 
class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel = 0):
        cmd1 = 4 | 2 | (( channel & 4) >> 2)
        cmd2 = (channel & 3) << 6
 
        adc = self.spi.xfer2([cmd1, cmd2, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()