import json

class ReadConfig():
    
    def __init__(self, filename):
        self.__file_config = open(filename)
        self.data=json.load(self.__file_config)
        self.__file_config.close()
    
    def get_db_name(self):
        return self.data["database"]["name"]
    def get_db_host(self):
        return self.data["database"]["host"]
    def get_db_user(self):
        return self.data["database"]["user"]
    def get_db_passwd(self):
        return self.data["database"]["password"]
    def get_db_port(self):
        return self.data["database"]["port"]
    
