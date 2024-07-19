import usocket as socket
from config import get_config
import uasyncio as asyncio
import ujson as json

from relays import get_relays_config, edit_relay_config, get_relays_pins, relay_pin_status

def init_webserver():
    CONFIG = get_config()
    port = CONFIG['webserver']['port']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    s.setblocking(False)
    print("[WEB] Listening on port: ", port)
    return s

async def serve_client(s):
    while True:
        try:
            conn, addr = s.accept()
            print('[WEB] Connection from %s' % str(addr))

            request = conn.recv(1024)
            request_str = request.decode('utf-8')

            # Parse the request method and path
            method = request_str.split(' ')[0]
            path = request_str.split(' ')[1][1:].split('/')
            body = request_str.split('\r\n')[-1]

            if body:
                body = json.loads(body)

            code = 200
            response_data = False

            if path[0] == 'relays':
                resp = relays_req(method, path, body)
                if resp == False:
                    code = 400
                    response_data = {"error": "Incorrect request"}
                else:
                    response_data = resp
            elif path[0] == 'config':
                resp = config_req(method, body)
                if resp == False:
                    code = 400
                    response_data = {"error": "Incorrect request"}
                else:
                    response_data = resp
            else:
                # Endpoint not found
                code = 404
                response_data = {"error": "Not Found"}

            if resp == False:
                code = 400
                response_data = {"error": "Incorrect request"}
            else:
                response_data = resp


            response_json = json.dumps(response_data)

            response = (
                'HTTP/1.1 {}\r\n'
                'Content-Type: application/json\r\n'
                'Content-Length: {}\r\n'
                '\r\n'
                '{}'
            ).format(code, len(response_json), response_json)
            conn.sendall(response.encode('utf-8'))

            # response = 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\nGPIO State: ' + gpio_state
            # conn.send(response)
            conn.close()
        except OSError:
            await asyncio.sleep(0.1)

def relays_req(method, path, body = False):
    relayid = False
    if len(path) > 2:
        relayid = path[2]

    if len(path) == 1: return False

    if path[1] == 'config':
        if method == 'GET':
            return get_relays_config(relayid)
        elif method == 'POST':
            if not body: return False
            if not relayid: return False

            return edit_relay_config(relayid)
    elif path[1] == 'pins':
        if method == 'GET':
            return get_relays_pins(relayid)
    else:
        # ASSUME RELAY ID
        relayid = path[1]

        if len(path) >= 2:
            submet = path[2]

            if submet == 'pin':
                if method == 'POST':
                    if not body: return False

                    if not 'status' in body: return False

                    status = body['status']

                    return relay_pin_status(relayid, status)

    # OPEARATIONS WITH ONE RELAY
    if len(path) < 4: return False
        
def config_req(method, body = False):

    if method == 'GET':
        return get_config()
    elif method == 'POST':
        # EDIT CONFIG
        return get_config()