from gpiozero import OutputDevice


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