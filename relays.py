from config import get_config
from machine import Pin

def get_relays_config(relayid = False):
    CONFIG = get_config()
    if not CONFIG: return False

    if not 'relays' in CONFIG: return False

    relays = CONFIG['relays']

    if relayid:
        if not relayid in relays: return False

        return relays[relayid]

    return relays

def edit_relay_config(relayid):
    if not relayid: return False

    # EDIT FILE
    return get_config()

def get_relays_pins(relayid = False):
    CONFIG = get_config()
    if not CONFIG: return False

    if not 'relays' in CONFIG: return False

    relays = CONFIG['relays']

    def get_pin_val(pin):
        val = Pin(pin, Pin.OUT).value()

        print(pin, val)

        retval = True
        if val == 0 or val == '0':
            retval =  False

        return retval

    if relayid:
        if not relayid in relays: return False

        relay = relays[relayid]
        pin = relay['pin']

        return get_pin_val(pin)
    
    all_pins = {};
    for relaykey in relays:
        relay = relays[relaykey]

        pin = relay['pin']

        all_pins[relaykey] = get_pin_val(pin)

    return all_pins

def relay_pin_status(relayid, status):
    val = 1

    if status == False: val = 0

    # GET RELAY PIN
    CONFIG = get_config()
    if not CONFIG: return False

    if not 'relays' in CONFIG: return False

    relays = CONFIG['relays']

    if not relayid in relays: return False

    relay = relays[relayid]

    pin = Pin(relay['pin'], Pin.OUT)

    pin.value(val)

    return pin.value()
