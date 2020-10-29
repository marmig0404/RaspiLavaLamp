import neopixel

class LightController:

    def __init__(self, pin, num_lights):
        self.pin = pin
        self.num_lights = num_lights
        self.lights = neopixel.NeoPixel(pin, num_lights, auto_write=False)
        self.light_state = False
        self.color_state = '#000000'

    def turn_on(self):       
        [r, g, b] = self.rgb_from_hex(self.color_state)
        print('turning on:')
        print(self.color_state)
        print([r,g,b])
        for i in range(self.num_lights):
            self.lights[i] = (r,g,b)
        self.lights.show()

    def turn_off(self):
        print('turning off')
        for i in range(self.num_lights):
            self.lights[i] = (0,0,0)
        self.lights.show()

    def change_color(self, color):
        print('changing color:')
        print(color)
        self.color_state = color
        print('confirm change')
        print(self.color_state)

    @staticmethod
    def rgb_from_hex(hex_color):
        hex_color = hex_color.replace("#", '')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
