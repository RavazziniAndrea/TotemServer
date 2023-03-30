from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn
import datetime 
import database_handler


app = FastAPI()

@app.post("/files/")
async def salva_file(img: UploadFile = File(...)):
    salvataggio = salva_filesystem(img)
    scrittura_db = salva_db(img.name)

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

#async def create_file(img: UploadFile = File(...)):
#    with open("files/newgatto.jpg","wb") as buff:
#        shutil.copyfileobj(img.file, buff)
#        
#    print("Arrivato, grande: "+img.filename)
#    return {"filename": img.filename}


@app.get("/")
async def root():
    #TODO
    #add_get_db(get_now())
    return FileResponse(path="./gatto.jpeg",filename="./gatto.jpeg",media_type='image/jpeg')


def get_photo_name():
    curr = datetime.datetime.now()
    #Impossible name duplication(?)
    return curr.strftime("%Y%m%d_%H-%M-%S")


if __name__ == "__main__":
    print("-- Start server --")
    print(f"Data: {get_photo_name()}")
    database_handler.get_conf()
    #uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)
