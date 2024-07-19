logTypes = {
    'error': {
        'title': '[ERROR]'
    },
    'info': {
        'title': '[INFO]'
    }
}

def log_debug(type, txt, addKey = ''):
    if not type or not txt: return False

    if not type in logTypes: return False

    #  TIME?
    log_title = logTypes[type]['title']
    add_key_str = '[' + str(addKey) + ']' if addKey else ''
    str = log_title + add_key_str + ' ' + str(txt)

    print(str)

    # LOG INTO SD CARD FILE

    return True

def log_vals():
    return