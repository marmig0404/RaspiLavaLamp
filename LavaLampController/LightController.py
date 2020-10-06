import board
import neopixel


class LightController:
    light_state = False
    color_state = '#000000'

    def __init__(self):
        self.lights = neopixel.NeoPixel(board.D18, 12, auto_write=False)

    def turn_on(self):
        [r, g, b] = self.color_from_hex(self.color_state)
        for light in self.lights:
            light.fill(r, g, b, 100)
        self.lights.show()

    def turn_off(self):
        for light in self.lights:
            light.fill(0, 0, 0, 0)
        self.lights.show()

    def change_color(self, color):
        self.color_state = color
        self.turn_on()

    @staticmethod
    def color_from_hex(hex_color):
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
