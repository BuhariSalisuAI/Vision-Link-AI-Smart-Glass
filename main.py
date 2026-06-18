from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

# 1. Janyo fayilolin ayyukan AI dinka
from ocr_reader import OCRReader
from navigation import NavigationSystem

# 2. Kirkirar sabar API
app = FastAPI()

class Waje(BaseModel):
    unguwa: str

# Kofa ta 0: Gwajin Sabar
@app.get("/")
def home():
    return {"message": "Vision-Link AI is Live and Running!"}

# ==========================================
# SABON TSARIN KOFAR KARATU (Tana karbar hoto yanzu)
# ==========================================
@app.post("/karatu")
async def karanta_rubutu(hoto: UploadFile = File(...)):
    try:
        # 1. Ajiye hoton da aka turo na wucin gadi a cikin sabar
        file_location = f"temp_{hoto.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(hoto.file, buffer)
        
        # 2. Mika hoton zuwa ga aikin OCR don ya karanta rubutun
        text = OCRReader().read_text(file_location) 
        
        # 3. Goge hoton daga sabar bayan an gama karantawa (don kar ya cika mana waje)
        os.remove(file_location)
        
        return {"sakamako": text, "matsayi": "An yi nasara"}
        
    except Exception as e:
        return {"sakamako": f"Akwai kuskure wajen karanta hoto: {str(e)}", "matsayi": "Kuskure"}

# Kofa ta 2: Bayar da Hanya
@app.post("/hanya")
def bada_hanya(waje: Waje):
    directions = NavigationSystem().get_directions(waje.unguwa)
    return {"sakamako": directions, "matsayi": "An yi nasara"}

# Kofa ta 3: Gane Abubuwa
@app.post("/abubuwa")
def gane_abubuwa():
    return {"sakamako": "Na gano Kujera, Mutum da Kwamfuta", "matsayi": "Gwajin Kofa"}
