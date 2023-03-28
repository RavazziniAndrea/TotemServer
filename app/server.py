from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn
import datetime 

app = FastAPI()

@app.post("/files/")
async def salva_file(img: UploadFile = File(...)):
    salvataggio = salva_filesystem(img)
    scrittura_db = salva_db(img.name)

def salva_filesystem(img):
    try:
        with open("files/"+get_photo_name()+".jpg","wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        print("File written: "+img.name)
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
    curr = get_now() 
    #Impossible name duplication(?)
    return (str(curr.year)+str(curr.month)+str(curr.day)+"_"+str(curr.hour)+'-'+str(curr.minute)+'-'+str(curr.second))

def get_now():
    return datetime.datetime.now()

if __name__ == "__main__":
    print("-- Start server --")
    print("Data: "+get_photo_name())
    #uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)
