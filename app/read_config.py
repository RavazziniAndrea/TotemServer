import json

def read_config():
    
    def __init__(self, filename):
        self.__file_config = open(filename, "r")
        self.data=json.loads(self.__file_config)
    
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
    
