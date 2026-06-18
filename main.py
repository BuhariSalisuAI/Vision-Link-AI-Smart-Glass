from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
from PIL import Image
import io
import base64
import urllib.request
import os
import uvicorn

app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.2.2")

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

PROTOTXT_PATH = "deploy.prototxt"
MODEL_PATH = "mobilenet_iter_73000.caffemodel"

def download_models():
    if not os.path.exists(PROTOTXT_PATH):
        url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt"
        urllib.request.urlretrieve(url, PROTOTXT_PATH)
    if not os.path.exists(MODEL_PATH):
        url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/mobilenet_iter_73000.caffemodel"
        urllib.request.urlretrieve(url, MODEL_PATH)

@app.get("/")
async def home():
    return {"sako": "Sabar Vision-Link AI tana aiki lafiya a kan Railway! 🚀"}

@app.post("/abubuwa", summary="Gane Abubuwa da Kyamara")
async def gane_abubuwa(hoto: UploadFile = File(...)):
    try:
        download_models()
        contents = await hoto.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        abubuwan_da_aka_gani = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.4:
                class_id = int(detections[0, 0, i, 1])
                object_name = CLASSES[class_id]
                if object_name not in abubuwan_da_aka_gani:
                    abubuwan_da_aka_gani.append(object_name)

        if not abubuwan_da_aka_gani:
            fada_da_baki = "Ban gano komai ba a gabanka"
        else:
            gajeren_rubutu = ", ".join(abubuwan_da_aka_gani)
            fada_da_baki = f"Ina gani {gajeren_rubutu}"

        from gtts import gTTS
        fayil_sauti = "gane_abubuwa.mp3"
        tts = gTTS(text=fada_da_baki, lang='ha', slow=False)
        tts.save(fayil_sauti)

        with open(fayil_sauti, "rb") as f:
            audio_encoded = base64.b64encode(f.read()).decode("utf-8")

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
        <body style="margin:0; padding:40px 20px; font-family:Arial; text-align:center; background:#f4f6f9;">
            <div style="background:white; padding:30px; border-radius:15px; box-shadow:0 4px 15px rgba(0,0,0,0.1); max-width:400px; margin:0 auto;">
                <h2 style="color:#1b5e20;">👓 Vision-Link AI Glasses</h2>
                <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
                <p style="font-size:18px; color:#333; font-weight:bold;">"{fada_da_baki}"</p>
                <audio controls autoplay style="width:100%;">
                    <source src="data:audio/mp3;base64,{audio_encoded}" type="audio/mp3">
                </audio>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h3>An samu matsala: {str(e)}</h3>")

# Wannan bangaren zai bawa Railway damar saita Port da kanta
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
               
