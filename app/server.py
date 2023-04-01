from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn
import datetime 
import pathlib
import os
import traceback
from database_handler import DatabaseHandler
from read_config import ReadConfig
from string_converter import StringConverter


app = FastAPI()
db_handler = None
CONFIG_PATH = "./app/config"
PHOTO_FOLDER = "./photos"

# ----------------------------------------------------------
# FASTAPI
# ----------------------------------------------------------
@app.post("/photo/")
async def salva_file(img: UploadFile = File(...)):
    salvataggio = salva_filesystem(img)
    scrittura_db = salva_db(img.name)



@app.get("/get/{photo_name}")
async def get_photo(photo_name):

    name = converter.decrypt(photo_name)

    #TODO sarebbe bello usare dei threads per le scritture a db così non rallentano il ritorno del file
    global db_handler
    db_handler.file_get_add_entry(datetime.datetime.now())

    db_handler.get_photo_from_name(name)

    #TODO inviare risposta al client ti togliere il QR dallo schermo (?)

    return FileResponse(path="./gatto.jpeg",filename="./gatto.jpeg",media_type='image/jpeg')

# ----------------------------------------------------------
# END - FASTAPI
# ----------------------------------------------------------


def salva_filesystem(img):
    try:
        with open(f"files/{get_photo_name()}.jpg","wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        print(f"File written: {img.name}")
        return True
    except Exception as e:
        print("Error writing file!!")
        print(traceback.print_exc())
        return False

def salva_db(path):
    #TODO 
    return True

def get_photo_name():
    curr = datetime.datetime.now()
    #Impossible name duplication(?)
    return curr.strftime("%Y%m%d_%H-%M-%S")


if __name__ == "__main__":
    print(" -- Start server --")
    print(f" -- {datetime.datetime.now()} --")

    try:
        converter = StringConverter(f"{CONFIG_PATH}/key")
        config = ReadConfig(f"{CONFIG_PATH}/db_config.json")
        db_handler = DatabaseHandler(config)

    except Exception as e:
        print("[ABORT] Cannot run server...")
        print(traceback.print_exc())
        quit()

    #uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)
