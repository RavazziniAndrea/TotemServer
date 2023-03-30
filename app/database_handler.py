import psycopg2


class DatabaseHandler():
    
    def __init__(self,config):
        self.database   = config.get_db_name()
        self.host       = config.get_db_host()
        self.user       = config.get_db_user()
        self.password   = config.get_db_passwd()
        self.port       = config.get_db_port()


    def file_get_add_entry(self, now):
        connection = self.__get_connection()
        cursor = connection.cursor()
        try:
            insert_statement = "INSERT INTO orari_download (%s) VALUES (%s)"
            cursor.execute(insert_statement, ("dataora",now)) #TODO sarà da testare e far funzionare
        except:
            #TODO
            print("ERRORRE Insert")


    def __get_connection(self):
        connection = psycopg2.connect(
                                database = self.database,
                                host     = self.host,
                                user     = self.user,
                                password = self.password,
                                port     = self.port)
        return connection
    



