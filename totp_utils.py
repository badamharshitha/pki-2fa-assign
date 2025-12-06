import base64
import pyotp

def hex_to_base32(hex_seed):
    return base64.b32encode(bytes.fromhex(hex_seed)).decode()

def generate_totp(hex_seed):
    seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(seed, digits=6, interval=30)
    return totp.now()

def verify_totp(hex_seed, code):
    seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(seed, digits=6, interval=30)
    return totp.verify(code, valid_window=1)

