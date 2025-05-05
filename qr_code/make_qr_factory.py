import segno
from segno import helpers
import io

def generate_qr_code(qr_type, information, config):
    buffer = io.BytesIO()
    qr = None

    try:
        print(f"Creating QR for type: {qr_type}")

        # Basic types using segno helpers
        if qr_type == 'string':
            qr = segno.make(information.get("string"))

        elif qr_type == 'url':
            qr = segno.make(information.get("url"))

        elif qr_type == 'wifi_connect':
            qr = helpers.make_wifi(
                ssid=information.get('ssid'),
                password=information.get('password'),
                security=information.get('security')
            )

        elif qr_type == 'mecard':
            qr = helpers.make_mecard(
                name=information.get('name'),
                email=information.get('email'),
                url=information.get('url')
            )

        elif qr_type == 'vcard':
            qr = helpers.make_vcard(
                name=information.get('name'),
                displayname=information.get('displayname'),
                email=information.get('email'),
                url=information.get('url')
            )

        elif qr_type == 'geoLocation':
            qr = helpers.make_geo(
                latitude=information.get('latitude'),
                longitude=information.get('longitude')
            )

        elif qr_type == 'epc':
            qr = helpers.make_epc_qr(
                name=information.get('name'),
                iban=information.get('iban'),
                amount=information.get('amount'),
                text=information.get('text'),
                encoding=information.get('encoding')
            )

        if qr is None:
            print(f"[Error] QR type '{qr_type}' not supported.")
            return None

        # Apply configuration
        qr.save(
            buffer,
            kind='png',
            scale=config.get('scale', 4),
            border=config.get('border', 1),
            dark=config.get('dark', 'black'),
            light=config.get('light', 'white'),
            data_dark=config.get('data_dark'),
            data_light=config.get('data_light')
        )

        return buffer

    except segno.DataOverflowError as e:
        print(f"[DataOverflowError] Content too large for QR code: {e}")
        return None

    except Exception as e:
        print(f"[Unexpected Error] {e}")
        return None
