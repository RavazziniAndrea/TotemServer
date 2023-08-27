import atexit
import base64
import datetime
import random
import string
import traceback
from typing import Tuple

import psycopg2

from constants import EXTENSION, PHOTO_FOLDER


# noinspection SqlNoDataSourceInspection
class DatabaseHandler:
    def __init__(self, config):
        self.database = config.get_db_name()
        self.host = config.get_db_host()
        self.user = config.get_db_user()
        self.password = config.get_db_passwd()
        self.port = config.get_db_port()
        self.__connection = None
        atexit.register(self.close_connection)

    def add_new_photo(self) -> Tuple[str, str]:
        name, path, digest = self.get_next_image_metadata()
        insert_statement = """INSERT INTO totem.photo (photoName,localPath,digest) VALUES (%s,%s,%s)"""
        self.__database_operation(insert_statement, (name, path, digest))
        return name, digest

    def get_next_image_metadata(self) -> Tuple[str, str, str]:
        # ID is 8-characters random alpha-numeric (a-z, A-Z, 0-9)
        # Image name is <id>_<current_time>
        # Digest is base64 encoding of image name
        id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        curr_time = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
        img_name = f"{id}_{curr_time}"
        path = str(PHOTO_FOLDER / (img_name + EXTENSION))
        digest = base64.b64encode(bytes(img_name, 'utf-8')).decode('utf-8')
        return img_name, path, digest

    def file_add_get_photo(self, name, digest):
        insert_statement = """INSERT INTO totem.downloadtime (photoName) VALUES (%s)"""
        self.__database_operation(insert_statement, (name,))
        update_statement = "UPDATE totem.photo SET downloaded = true WHERE digest=%s"
        self.__database_operation(update_statement, (digest,))

    def get_image_path_from_digest(self, digest):
        try:
            select_statement = """SELECT photoName FROM totem.photo WHERE digest=%s"""
            res = self.__database_operation(select_statement, (digest,), True)
            # NOTE: we de-reference two times because `res` is a list of tuples, e.g. [(path,)]
            return res[0][0]
        except:
            traceback.print_exc()
            return False

    def is_already_downloaded(self, digest):
        try:
            select_statement = "SELECT downloaded FROM totem.photo WHERE digest=%s"
            res = self.__database_operation(select_statement, (digest,), True)
            # NOTE: we de-reference two times because `res` is a list of tuples, e.g. [(False,)]
            return res[0][0]
        except:
            traceback.print_exc()
            return False

    def __database_operation(self, statement, values=None, get_results=False):
        connection = self.__get_connection()
        cursor = connection.cursor()
        res = None
        try:
            cursor.execute(statement, values)
            connection.commit()
            if get_results:
                res = cursor.fetchall()
        except Exception as e:
            print(f"Error with statement:\n"
                  f"`{statement}`\n"
                  f"with values:\n"
                  f"`{values}`\n"
                  f"Error: {e}")

        cursor.close()
        return res

    def __get_connection(self):
        connection = psycopg2.connect(
            database=self.database,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port)
        return connection

    def close_connection(self):
        try:
            self.__connection.close()
        except:
            print("Connection already closed")
