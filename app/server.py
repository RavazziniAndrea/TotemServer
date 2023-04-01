from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn
import datetime 
import pathlib
import os
import traceback
from threading import Thread
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
    salvataggio = salva_filesystem(img) #TODO se ritorna False, fai qualcosa, non andare avanti tipo...
    scrittura_db = salva_db(img.name)


@app.get("/get/{photo_name}")
async def get_photo(photo_name):

    name = converter.decrypt(photo_name)

    #TODO bisogna testarlo :)
    # global db_handler
    # db_handler.file_get_add_entry(name)
    thread = Thread(target=db_handler.file_get_add_entry, args=name)
    thread.start()

    #TODO inviare risposta al client ti togliere il QR dallo schermo (?)

    return FileResponse(path=f"{PHOTO_FOLDER}/{name}",filename=f"{PHOTO_FOLDER}/{name}",media_type='image/jpeg')

# ----------------------------------------------------------
# END - FASTAPI
# ----------------------------------------------------------


def salva_filesystem(img):
    try:
        with open(f"{PHOTO_FOLDER}/{get_photo_name()}.jpg","wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        print(f"File written: {img.name}")
        return True
    except Exception as e:
        print("Error writing file!!") #TODO gestisci meglio questa eccezione! (magari tornando qualcosa al client)
        print(traceback.print_exc())
        return False


def salva_db(name):
    db_handler.add_new_photo(name, PHOTO_FOLDER+name, converter.encrypt(name))
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
