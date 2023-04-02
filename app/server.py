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


CONFIG_PATH  = "./app/config"
KEY_PATH     = f"{CONFIG_PATH}/key"
PHOTO_FOLDER = "./photos"
MEDIA_TYPE   = "image/jpeg"
EXTENSION    = ".jpg"


# ----------------------------------------------------------
# FASTAPI
# ----------------------------------------------------------

app = FastAPI()

@app.post("/photo/")
async def salva_file(img: UploadFile = File(...)):
    try:
        salva_filesystem(img) #TODO se exception, fai qualcosa, non andare avanti tipo...
        salva_db(img.name)
    except Exception as e:
        #TODO tornare qualcosa al client
        print(traceback.print_exc)


@app.get("/get/{photo_name}")
async def get_photo(photo_name):
    global converter
    global db_handler
    name = StringConverter.decrypt(photo_name)

    #TODO bisogna testarlo :)
    thread_add_get_photo = Thread(target=db_handler.file_add_get_photo, args=name)
    thread_add_get_photo.start()
    #TODO inviare risposta al client ti togliere il QR dallo schermo (?)

    return FileResponse(path=f"{PHOTO_FOLDER}/{name}",filename=f"{PHOTO_FOLDER}/{name}",media_type=MEDIA_TYPE)

# ----------------------------------------------------------
# END - FASTAPI
# ----------------------------------------------------------


def salva_filesystem(img):
    try:
        with open(f"{PHOTO_FOLDER}/{get_photo_name()}{EXTENSION}","wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        print(f"File written: {img.name}")
    except Exception as e:
        print("Error writing file!!") #TODO gestisci meglio questa eccezione! (magari tornando qualcosa al client)
        print(traceback.print_exc())
        raise Exception("Not written in filesystem")


def salva_db(name):
    global converter
    global db_handler
    db_handler.add_new_photo(name, PHOTO_FOLDER+name, StringConverter.encrypt(name))


def get_photo_name():
    curr = datetime.datetime.now()
    #Impossible name duplication(?)
    return curr.strftime("%Y%m%d_%H-%M-%S")


if __name__ == "__main__":
    print(" -- Start server --")
    print(f" -- {datetime.datetime.now()} --")

    global converter
    global db_handler
    try:
        converter = StringConverter(f"{CONFIG_PATH}/key")
        config = ReadConfig(f"{CONFIG_PATH}/db_config.json")
        db_handler = DatabaseHandler(config)

    except Exception as e:
        print("[ABORT] Cannot run server...")
        print(traceback.print_exc())
        quit()

    uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)
