import segno
from segno import helpers
import io

def generate_qr_code(type, information, config):
    buffer = io.BytesIO()

    if type == 'string':
        print(f"creating {type}")
        qr = segno.make(information, version=1)
    elif type == 'wifi_connect':
        print(f"creating {type}")
        qr = helpers.make_wifi(ssid=information.get('ssid'), password=information.get('password'), security=information.get('security'))
    elif type == 'mecard':
        print(f"creating {type}")
        qr = helpers.make_mecard(name=information.get('name'), email=information.get('email'), url=information.get('url'))
    elif type == 'vcard':
        print(f"creating {type}")
        qr = helpers.make_vcard(name=information.get('name'), displayname=information.get('displayname'), email=information.get('email'), url=information.get('url'))
    elif type == 'geoLocation':
        print(f"creating {type}")
        latitude,longitude=information.get('longitude'),information.get('latitude'), 
        qr = helpers.make_geo(latitude, longitude)
    elif type == 'epc':
        print(f"creating {type}")
        qr = helpers.make_epc_qr(name=information.get('name'), iban=information.get('iban'), amount=information.get('amount'), text=information.get('text'), encoding=information.get('encoding'))
    else:
        return None
    scale = config.get('scale', 4)
    border = config.get('border', 1)
    dark = config.get('dark', 'black')
    light = config.get('light', 'white')
    data_dark = config.get('data_dark', None)
    data_light = config.get('data_light', None)

    qr.save(buffer, kind='png',scale=scale, border=border, dark=dark, light=light, data_dark=data_dark, data_light=data_light)

    return buffer

# # Example usage
# params = {
#     'type': 'wifi_connect',
#     'information': {'ssid': 'My network', 'password': 'secret', 'security': 'WPA'},
#     'configuration': {'filename': 'qrcode_yellow-submarine.png', 'scale': 4, 'unit': 'mm', 'border': 1, 'dark': 'darkred', 'light': 'lightblue', 'data_dark': 'darkorange', 'data_light': 'yellow'}
# }

