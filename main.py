from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pytesseract
from PIL import Image
import io
import os

# Bayanin asali na API din
app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.1.0")

# Tsarin karbar rubutu daga wajen mai amfani
class RubutunSauti(BaseModel):
    rubutu: str

@app.get("/")
async def home():
    return {"sako": "Sabar Vision-Link tana aiki lafiya! 🚀"}

@app.post("/karatu", summary="Karanta Rubutu")
async def karanta_rubutu(hoto: UploadFile = File(...)):
    try:
        contents = await hoto.read()
        image = Image.open(io.BytesIO(contents))
        
        # Ciro rubutu daga hoton (OCR)
        rubutu = pytesseract.image_to_string(image, lang='eng')
        
        return {"sakamako": rubutu.strip(), "matsayi": "yayi"}
    except Exception as e:
        return {"sakamako": None, "matsayi": f"An samu matsala: {str(e)}"}

@app.post("/hanya", summary="Bada Hanya")
async def bada_hanya(hoto: UploadFile = File(...)):
    return {"sakamako": "Wannan kofar gane hanya ce", "matsayi": "yayi"}

@app.post("/abubuwa", summary="Gane Abubuwa")
async def gane_abubuwa(hoto: UploadFile = File(...)):
    return {"sakamako": "Wannan kofar gane abubuwa ce", "matsayi": "yayi"}

@app.post("/sauti", summary="Maida Rubutu Sauti")
async def maida_rubutu_sauti(bayanai: RubutunSauti):
    try:
        from gtts import gTTS
        fayil_sauti = "sakamako_sauti.mp3"
        
        # Amfani da Google TTS tare da harshen Hausa ('ha') mai dadi
        tts = gTTS(text=bayanai.rubutu, lang='ha', slow=False)
        tts.save(fayil_sauti)
        
        # Mun cire filename don ya ba ka damar danna Play (▶️) kai tsaye a shafin gwaji
        return FileResponse(fayil_sauti, media_type="audio/mp3")
    except Exception as e:
        return {"matsala": f"An samu matsala wajen juyawa zuwa sauti: {str(e)}"}
