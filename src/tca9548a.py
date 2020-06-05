# This is the driver for the TCA9548A I2C multiplexer.
# There is a driver on github, but it didn't work for me.
# After some search, I found this on the micropython forum. It's much smaller and it works great.
# Here is the link to the thread: https://forum.micropython.org/viewtopic.php?f=2&t=6284&p=40408&hilit=tca9548a#p40408
# All credit for this driver goes to user "sequel" on the micropython forum (forum.micropython.org)!


import machine
import ustruct


class TCA9548A():
    def __init__(self, scl_pin, sda_pin, address):
        self.address = address
        self.bus = machine.I2C(-1, machine.Pin(scl_pin), machine.Pin(sda_pin))

    def switch_channel(self, channel):
        self.bus.writeto(self.address, ustruct.pack('B', 1 << channel))
