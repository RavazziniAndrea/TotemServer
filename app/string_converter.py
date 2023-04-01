from cryptography.fernet import Fernet


class StringConverter():

    def __init__(self, key_path):
        try:
            print(key_path)
            self.key = open(key_path,"r").readline()
            if self.key == None or self.key == "":
                raise Exception
        except Exception as e:
            raise Exception(e)

        self.fernet = Fernet(self.key)


    def encrypt(self, to_encrypt):
        return self.fernet.encrypt(to_encrypt.encode())


    def decrypt(self, to_decrypt):
        return self.fernet.decrypt(to_decrypt).decode()
