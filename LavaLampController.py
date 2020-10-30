import socketserver
import board
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Tuple
from time import sleep

from LightController import LightController
from TempController import TempController

host_name = '192.168.1.45' # change based on DHCP
host_port = 8000
target_temp = 40
heater_pin = 10
sensor_pin = 17
light_pin = board.D18
num_lights = 12

post_mem = {"heater": "off",
                         "lamp": "off",
                         "color": "#FF0000"}


light_controller = LightController(light_pin, num_lights)  # create light controller
temp_controller = TempController(target_temp, heater_pin, sensor_pin)  # create temp 

class LampServer(BaseHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer) -> None:
        self.heater_thread_stop = False
        self.heater_thread = Thread(target=self.run_heater, args=(lambda: self.heater_thread_stop,))
        self.light_controller = light_controller
        self.temp_controller = temp_controller
        super().__init__(request, client_address, server)


    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>Lava Lamp Controller</h1>
            <p>Current Lamp temperature is {}C</p>
            <form action="/" method="POST">
                Turn Heater :
                <input type="submit" name="heater" value="On">
                <input type="submit" name="heater" value="Off">
            </form>
            <form action="/" method="POST">
                Turn Lamp :
                <input type="submit" name="lamp" value="On">
                <input type="submit" name="lamp" value="Off">
                <input type="color" name="color" value={}>
            </form>
            </body>
            </html>
        '''
        self.do_HEAD()
        self.wfile.write(html.format(self.temp_controller.read_temp(), post_mem.get('color')).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
        post_data = post_data.split("&")
        for data in post_data:
            split_data = data.split("=")
            post_mem[split_data[0]] = split_data[1]
        self.do_action()
        self._redirect('/')  # Redirect back to the root url

    def do_action(self):
        action_switch = {
            "heater": self.change_heater_state(),
            "lamp": self.change_lamp_state(),
            "color": self.change_color_state(),
        }
        for pair in post_mem:
            return action_switch.get(pair[0])

    def change_heater_state(self):
        state = post_mem.get('heater')
        if state == "On":
            self.heater_thread_stop = False
            self.heater_thread.start()
        else:
            self.heater_thread_stop = True

    def change_lamp_state(self):
        state = post_mem.get('lamp')
        if state == "On":
            self.light_controller.turn_on()
        else:
            self.light_controller.turn_off()

    def change_color_state(self):
        state = post_mem.get('color')
        state = state.replace('%23', '#')  # make standard hex color code
        post_mem['color'] = state
        print('applying color change')
        print(state)
        self.light_controller.change_color(state)
        
    def run_heater(self, stop):
        while True:
            self.temp_controller.update()
            sleep(10)
            if stop():
                break


http_server = HTTPServer((host_name, host_port), LampServer)
print("Server Starts - %s:%s" % (host_name, host_port))

try:
    http_server.serve_forever()
except KeyboardInterrupt:
    http_server.server_close()
