from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pytesseract
from PIL import Image
import io
import os

# Bayanin asali na API din
app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.1.0")

# Tsarin karbar rubutu daga wajen mai amfani don juyawa ya zama sauti
class RubutunSauti(BaseModel):
    rubutu: str

@app.get("/")
async def home():
    return {"sako": "Sabar Vision-Link tana aiki lafiya! 🚀"}

@app.post("/karatu", summary="Karanta Rubutu")
async def karanta_rubutu(hoto: UploadFile = File(...)):
    try:
        # Karanta hoton da aka turo
        contents = await hoto.read()
        image = Image.open(io.BytesIO(contents))
        
        # Ciro rubutu daga hoton (OCR) da turanci
        rubutu = pytesseract.image_to_string(image, lang='eng')
        
        return {"sakamako": rubutu.strip(), "matsayi": "yayi"}
    except Exception as e:
        return {"sakamako": None, "matsayi": f"An samu matsala: {str(e)}"}

@app.post("/hanya", summary="Bada Hanya")
async def bada_hanya(hoto: UploadFile = File(...)):
    # Wannan kofar gane hanya ce (Kamar yadda aka tsara a baya)
    return {"sakamako": "Wannan kofar gane hanya ce", "matsayi": "yayi"}

@app.post("/abubuwa", summary="Gane Abubuwa")
async def gane_abubuwa(hoto: UploadFile = File(...)):
    # Wannan kofar gane abubuwa ce (Kamar yadda aka tsara a baya)
    return {"sakamako": "Wannan kofar gane abubuwa ce", "matsayi": "yayi"}

@app.post("/sauti", summary="Maida Rubutu Sauti")
async def maida_rubutu_sauti(bayanai: RubutunSauti):
    try:
        # Sunan fayil din da zai ajiye muryar
        fayil_sauti = "sakamako_sauti.wav"
        
        # Tsabtace rubutun don gujewa matsalar 'quotes' a wajen umarni
        tsabtace_rubutu = bayanai.rubutu.replace('"', '').replace("'", "")
        
        # Amfani da injin eSpeak kai tsaye don hada sautin .wav
        os.system(f'espeak -w {fayil_sauti} "{tsabtace_rubutu}"')
        
        # Dawo da fayil din sautin don a ji a shafin gwaji (Swagger UI)
        return FileResponse(fayil_sauti, media_type="audio/wav", filename="murya.wav")
    except Exception as e:
        return {"matsala": f"An samu matsala wajen juyawa zuwa sauti: {str(e)}"}
