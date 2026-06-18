from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pytesseract
from PIL import Image
import io
import base64

app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.1.0")

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

# Mun maida shi GET domin ka iya budewa kai tsaye a burauzar wayarka
@app.get("/sauti", summary="Maida Rubutu Sauti")
async def maida_rubutu_sauti(rubutu: str = "Sannu babban injiniya Buhari"):
    try:
        from gtts import gTTS
        fayil_sauti = "sakamako_sauti.mp3"
        
        # Samar da sauti da Google TTS
        tts = gTTS(text=rubutu, lang='ha', slow=False)
        tts.save(fayil_sauti)
        
        # Saka sautin a cikin tsarin rubutu na base64
        with open(fayil_sauti, "rb") as f:
            audio_encoded = base64.b64encode(f.read()).decode("utf-8")
            
        # Kyakkyawan dandalin kunna sauti na musamman
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vision-Link Audio</title>
        </head>
        <body style="margin: 0; padding: 40px 20px; font-family: Arial, sans-serif; text-align: center; background-color: #f4f6f9;">
            <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 400px; margin: 0 auto;">
                <h2 style="color: #1b5e20; margin-bottom: 5px;">🔊 Vision-Link AI</h2>
                <p style="color: #666; font-size: 14px; margin-top: 0;">Smart Glasses Audio System</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                
                <p style="font-size: 16px; color: #333; font-weight: bold; margin-bottom: 25px;">
                    "{rubutu}"
                </p>
                
                <audio controls autoplay style="width: 100%; outline: none;">
                    <source src="data:audio/mp3;base64,{audio_encoded}" type="audio/mp3">
                    Wayarka bata iya kunna wannan sautin.
                </audio>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h3>An samu matsala: {str(e)}</h3>")
