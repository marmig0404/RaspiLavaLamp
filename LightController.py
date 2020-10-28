import neopixel

class LightController:

    light_state = False
    color_state = '#000000'

    def __init__(self, pin):
        self.lights = neopixel.NeoPixel(pin, 12, auto_write=False)

    def turn_on(self):
        [r, g, b] = self.rgb_from_hex(self.color_state)
        for light in self.lights:
            light.fill(r, g, b, 100)
        self.lights.show()

    def turn_off(self):
        for light in self.lights:
            light.fill(0, 0, 0, 0)
        self.lights.show()

    def change_color(self, color):
        self.color_state = color

    @staticmethod
    def rgb_from_hex(hex_color):
        hex_color = hex_color.replace("#", '')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
