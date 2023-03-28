import psycopg2
from app import read_config



def get_conf():
    config = read_config("db_config.json")
    print(config)
    print("Done")


# connection = psycopg2.connect(database=config.get,
#                               host="",
#                               user="",
#                               password="",
#                               port="")
