from cryptography.fernet import Fernet


class StringConverter():

    def __init__(self, key_path):
        try:
            print(key_path)
            self.key = open(key_path,"r").readline()
            print(f"STAMPO LA KEY: {self.key}")
            if self.key == None or self.key == "":
                print(f"va bene lo stessoooo: {self.key}")
                raise Exception
        except Exception as e:
            print(e)
            raise Exception("Can't load secret key")

        self.fernet = Fernet(self.key)

    def encrypt(self, to_encrypt):
        return self.fernet.encrypt(to_encrypt.encode())

    def decrypt(self, to_decrypt):
        return self.fernet.decrypt(to_decrypt).decode()
