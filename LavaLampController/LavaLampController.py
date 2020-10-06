from http.server import BaseHTTPRequestHandler, HTTPServer

from LavaLampController.LightController import LightController
from LavaLampController.TempController import TempController

host_name = 'localhost'
host_port = 8000


class LampServer(BaseHTTPRequestHandler):
    post_mem = {"heater": "off",
                "lamp": "off",
                "color": "#FF0000"}

    light_controller = LightController()
    temp_controller = TempController(40)

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
            <p>Current Lamp temperature is {}</p>
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
        self.wfile.write(html.format("69", self.post_mem.get('color')).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
        post_data = post_data.split("&")
        for data in post_data:
            split_data = data.split("=")
            self.post_mem[split_data[0]] = split_data[1]
        self.do_action()
        self._redirect('/')  # Redirect back to the root url

    def do_action(self):
        action_switch = {
            "heater": self.change_heater_state(),
            "lamp": self.change_lamp_state(),
            "color": self.change_color_state(),
        }
        for pair in self.post_mem:
            return action_switch.get(pair[0])

    def change_heater_state(self):
        state = self.post_mem.get('heater')
        if state == "On":
            print('Heater on')
        else:
            print('Heater off')

    def change_lamp_state(self):
        state = self.post_mem.get('lamp')
        if state == "On":
            print('Lamp on')
        else:
            print('Lamp off')

    def change_color_state(self):
        state = self.post_mem.get('color')
        state = state.replace('%23', '#')  # make standard hex color code
        self.post_mem['color'] = state
        print('Color:' + state)


http_server = HTTPServer((host_name, host_port), LampServer)
print("Server Starts - %s:%s" % (host_name, host_port))

try:
    http_server.serve_forever()
except KeyboardInterrupt:
    http_server.server_close()
