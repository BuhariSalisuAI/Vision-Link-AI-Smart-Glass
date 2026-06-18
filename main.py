from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import pytesseract
from PIL import Image
import io
import os
import base64

app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.1.0")

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
        
        # Hada sautin da Google TTS tare da harshen Hausa
        tts = gTTS(text=bayanai.rubutu, lang='ha', slow=False)
        tts.save(fayil_sauti)
        
        # Karanta fayil din sautin sannan mu canza shi zuwa base64 text
        with open(fayil_sauti, "rb") as f:
            audio_encoded = base64.b64encode(f.read()).decode("utf-8")
            
        # Samar da kyakkyawan player na HTML wanda zai fito radau a waya kai tsaye
        html_content = f"""
        <html>
            <body style="margin: 0; padding: 10px; font-family: sans-serif; text-align: center;">
                <h4 style="color: #2e7d32; margin-bottom: 10px;">🔊 Muryar Vision-Link Ta Shirya!</h4>
                <audio controls autoplay style="width: 100%; max-width: 300px;">
                    <source src="data:audio/mp3;base64,{audio_encoded}" type="audio/mp3">
                    Burauzar ka bata goyon bayan kunna sauti.
                </audio>
                <br><br>
                <p style="font-size: 12px; color: #666;">Rubutu: "{bayanai.rubutu}"</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h4>An samu matsala: {str(e)}</h4>")
