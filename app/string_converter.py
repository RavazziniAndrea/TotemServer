import base64

def encrypt(to_encrypt):
    return base64.b64decode(to_encrypt)

def decrypt(to_decrypt):
    return base64.b64decode(to_decrypt)
