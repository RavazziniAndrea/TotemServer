from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn

app = FastAPI()

@app.post("/files/")
async def salva_file(img: UploadFile = File(...)):
    salvata = salva_filesystem(img)
    scritta_db = salva_db(img.name)

def salva_filesystem(img):
    try:
        with open("files/nome_data_foto.jpg","wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        print("File scritto: "+img.name)
        return true
    except:
        print("Errore scrittura file!!")
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
    return FileResponse(path="./gatto.jpeg",filename="./gatto.jpeg",media_type='image/jpeg')


if __name__ == "__main__":
    print("-- Avvio server --")
    uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)
