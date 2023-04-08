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
        finally:
            if connection:
                cursor.close()
                connection.close()


    def file_add_get_photo(self, name):
        connection = self.__get_connection()
        cursor = connection.cursor()
        try:
            insert_statement = """INSERT INTO totem.downloadtime (photoName) VALUES (%s)"""
            cursor.execute(insert_statement, (name,)) #TODO sarà da testare e far funzionare
            connection.commit()
            update_statement = "UPDATE totem.photo SET downloaded = true WHERE photoName = %s"
            cursor.execute(update_statement, (name,)) #TODO sarà da testare e far funzionare
            connection.commit()
        except Exception as e:
            #TODO
            print("ERRORRE database")
            print(e)
            connection.rollback()
        finally:
            if connection:
                cursor.close()
                connection.close()


    def is_already_downloaded(self, name):
        connection = self.__get_connection()
        cursor = connection.cursor()
        try:
            select_statement = "SELECT downloaded FROM totem.photo WHERE photoname=%s"
            cursor.execute(select_statement, (name,))
            record = cursor.fetchall()
            if record.__len__ == 1:
                return record[0]
            else:
                #TODO gestire meglio
                return False
        except Exception as e:
            #TODO
            print("ERRORRE database")
            print(e)
        finally:
            if connection:
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
        finally:
            if connection:
                cursor.close()
                connection.close()
            
        connection.close()


    def __get_connection(self):
        connection = psycopg2.connect(
                                database = self.database,
                                host     = self.host,
                                user     = self.user,
                                password = self.password,
                                port     = self.port)
        return connection
    



