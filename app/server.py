from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn

app = FastAPI()

#@app.post("/files/")
#async def create_file(file: bytes = File()):
#    return {"file_size": len(file)}

@app.post("/files/")
async def create_file(img: UploadFile = File(...)):
    with open("files/newgatto.jpg","wb") as buff:
        shutil.copyfileobj(img.file, buff)
        
    print("Arrivato, grande: "+img.filename)
    return {"filename": img.filename}


@app.get("/")
async def root():
    return FileResponse(path="./gatto.jpeg",filename="./gatto.jpeg",media_type='image/jpeg')


if __name__ == "__main__":
    print("Avvio server-")
    uvicorn.run("server:app", host="0.0.0.0", port=10481, workers=3)