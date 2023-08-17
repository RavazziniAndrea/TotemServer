import datetime
import os
import shutil
import traceback

import uvicorn
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import FileResponse
# from string_converter import StringConverter
from pydantic import BaseModel

from constants import CONFIG_PATH, PHOTO_FOLDER, EXTENSION, MEDIA_TYPE
from database_handler import DatabaseHandler
from read_config import ReadConfig

try:
    # converter = StringConverter(f"{CONFIG_PATH}/key")
    config = ReadConfig(f"{CONFIG_PATH}/db_config.json")
    db_handler = DatabaseHandler(config)

except Exception as e:
    print("[ABORT] Cannot run server...")
    print(traceback.print_exc())
    quit()


class Item(BaseModel):
    res: str


# ----------------------------------------------------------
# FASTAPI
# ----------------------------------------------------------

app = FastAPI()


@app.post("/photo/")
async def salva_file(img: UploadFile, request: Request):
    ips = [x.strip() for x in os.environ.get('BB_WHITELIST_IP', '').split(',')]
    if ips:
        print(f"Request coming from: {request.client.host}\n"
              f"Whitelisted IPs: {ips}\n"
              f"{request.client.host in ips}")
    else:
        print(ips)
    try:
        global db_handler
        img_name, digest = db_handler.add_new_photo()
        salva_filesystem(img, img_name)
    except Exception as e:
        traceback.print_exc()
        digest = ""

    return Item(res=digest)


@app.get("/get/{photo_digest}")
async def get_photo(photo_digest):
    global db_handler
    if not db_handler.is_already_downloaded(photo_digest):
        img_name = db_handler.get_image_path_from_digest(photo_digest)
        db_handler.file_add_get_photo(img_name, photo_digest)

        path = PHOTO_FOLDER / (img_name + EXTENSION)
        if not path.exists():
            print(f"Il file non esiste, cazzo fai?")
            return Item(res="Il file non esiste, cheffai birbantello?")

        return FileResponse(path=path, media_type=MEDIA_TYPE)
    else:
        print("Foto già scaricata")
        return Item(res="Hai già scaricato la foto, se non sei stato tu fattela mandare o chiedi ai nerd dei BarBoun")


@app.get("/check/{photo_digest}")
async def check_photo_downloaded(photo_digest):
    global db_handler
    return Item(res=str(db_handler.is_already_downloaded(photo_digest)))


# ----------------------------------------------------------
# END - FASTAPI
# ----------------------------------------------------------


def salva_filesystem(img, img_name):
    try:
        with open(f"{PHOTO_FOLDER}/{img_name}{EXTENSION}", "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        # print(f"File written: {img.filename}")
    except Exception as e:
        print("Error writing file!!")
        traceback.print_exc()
        raise Exception("Not written in filesystem")


def main():
    print(" -- Start server --")
    print(f" -- {datetime.datetime.now()} --")

    uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)  # , proxy_headers=True


if __name__ == "__main__":
    main()
