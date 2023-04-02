from cryptography.fernet import Fernet
from server import KEY_PATH

class StringConverter():

    try:
        key = open(KEY_PATH,"r").readline()
        if key == None or key == "":
            raise Exception
    except Exception as e:
        raise Exception(e)

    fernet = Fernet(key)


    def encrypt(self, to_encrypt):
        return self.fernet.encrypt(to_encrypt.encode())


    def decrypt(self, to_decrypt):
        return self.fernet.decrypt(to_decrypt).decode()
