from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn
import datetime 
import pathlib
import os
from database_handler import DatabaseHandler
from read_config import ReadConfig
from string_converter import StringConverter


app = FastAPI()
db_handler = None
CONFIG_PATH = "/app/config"

# ----------------------------------------------------------
# FASTAPI
# ----------------------------------------------------------
@app.post("/files/")
async def salva_file(img: UploadFile = File(...)):
    salvataggio = salva_filesystem(img)
    scrittura_db = salva_db(img.name)

@app.get("/photo/{photo_id}")
async def get_photo(photo_id):
    #TODO sarebbe bello usare dei threads per le scritture a db così non rallentano il ritorno del file
    global db_handler
    db_handler.file_get_add_entry(datetime.datetime.now())

    #TODO decrypt photo_id
    id = ""
    db_handler.get_photo_path(id)

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
    except:
        print("Error writing file!!")
        return False

def salva_db(path):
    #TODO 
    return True

def get_photo_name():
    curr = datetime.datetime.now()
    #Impossible name duplication(?)
    return curr.strftime("%Y%m%d_%H-%M-%S")


if __name__ == "__main__":
    print("-- Start server --")
    print(f"Data: {get_photo_name()}")

    try:
        converter = StringConverter(f"{CONFIG_PATH}/key")
        config = ReadConfig(f"{CONFIG_PATH}/db_config.json")
        db_handler = DatabaseHandler(config)

        s=StringConverter.encrypt("ciaoneeee")
        print(s)
        print(StringConverter.decrypt(s))

    except Exception as e:
        print("[ABORT] Cannot run server...")
        print(e)
        quit()

    #uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)
