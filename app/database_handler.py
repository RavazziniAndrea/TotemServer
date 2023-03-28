import psycopg2
from read_config import ReadConfig



def get_conf():
    config = ReadConfig("db_config.json")
    print(config)
    print("Done")


# connection = psycopg2.connect(database=config.get,
#                               host="",
#                               user="",
#                               password="",
#                               port="")
