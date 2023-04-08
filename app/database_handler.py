import psycopg2
import traceback


class DatabaseHandler():
    
    def __init__(self,config):
        self.database   = config.get_db_name()
        self.host       = config.get_db_host()
        self.user       = config.get_db_user()
        self.password   = config.get_db_passwd()
        self.port       = config.get_db_port()


    def add_new_photo(self, name, path, digest):
        connection = self.__get_connection()
        cursor = connection.cursor()
        try:
            insert_statement = """INSERT INTO Photo (photoName,localPath,digested) VALUES (%s,%s,%s)"""
            cursor.execute(insert_statement, (name, path, digest)) #TODO sarà da testare e far funzionare
            connection.commit()
        except:
            #TODO
            print("ERRORRE Insert")
            connection.rollback()
        cursor.close()    
        connection.close()


    def file_add_get_photo(self, name):
        connection = self.__get_connection()
        cursor = connection.cursor()
        #FIXME non funziona la scrittura su db :(
        #adesso non si collega proprio, sarà un problema di network?
        try:
            cursor.execute("""SELECT count(*) FROM information_schema.tables """)
            for table in cursor.fetchall():
                print(table)    

            insert_statement = """SELECT * FROM totem.downloadtime"""
            cursor.execute(insert_statement)
            for val in cursor.fetchall():
                print(val) 

            print("Inizio insert")
            insert_statement = """INSERT INTO totem.downloadtime (photoName) VALUES (%s)"""
            cursor.execute(insert_statement, (name,)) #TODO sarà da testare e far funzionare
            connection.commit()
            print("Fine insert")
            print("Inizio Update")
            update_statement = "UPDATE totem.photo SET downloaded = true WHERE photoName = %s"
            cursor.execute(update_statement, (name,)) #TODO sarà da testare e far funzionare
            connection.commit()
            print("Fine Update")
        except Exception as e:
            #TODO
            print("ERRORRE database")
            print(e)
            connection.rollback()
        cursor.close()
        connection.close()


    #Unused...
    def __database_operation(self, statements, values):
        connection = self.__get_connection()
        cursor = connection.cursor()
        try:
            for statement in statements:
                cursor.execute(statement, values) #TODO sarà da testare e far funzionare
        except:
            #TODO
            print("ERRORRE Insert")
            
        connection.close()


    def __get_connection(self):
        connection = psycopg2.connect(
                                database = self.database,
                                host     = self.host,
                                user     = self.user,
                                password = self.password,
                                port     = self.port)
        return connection
    



