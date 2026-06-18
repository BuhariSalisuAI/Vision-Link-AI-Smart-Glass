from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
import base64
import urllib.request
import os
import uvicorn

app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.2.3")

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

@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h3>Sabar Vision-Link AI tana aiki lafiya! 🚀</h3>"

@app.post("/abubuwa", response_class=HTMLResponse)
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

        # Fassara zuwa Hausa ta gari
        if not abubuwan_da_aka_gani:
            fada_da_baki = "Ban gano komai ba a gabanka"
        else:
            // Gyaran fassara don makaho ya fahimta
            fassara = {"car": "mota", "person": "mutum", "bus": "babban mota", "motorbike": "babur"}
            fassarar_hausa = [fassara.get(obj, obj) for obj in abubuwan_da_aka_gani]
            gajeren_rubutu = ", ".join(fassarar_hausa)
            fada_da_baki = f"Ina gani {gajeren_rubutu}"

        # Samar da muryar Hausa
        from gtts import gTTS
        fayil_sauti = "sauti.mp3"
        tts = gTTS(text=fada_da_baki, lang='ha', slow=False)
        tts.save(fayil_sauti)

        with open(fayil_sauti, "rb") as f:
            audio_encoded = base64.b64encode(f.read()).decode("utf-8")

        # Karanta hoton asali don nuna shi a shafin tare da sauti
        _, encoded_img = cv2.imencode('.jpg', img)
        hoto_encoded = base64.b64encode(encoded_img).decode('utf-8')

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vision-Link AI Smart Glasses</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; background-color: #f4f6f9; margin: 0; padding: 20px; }}
                .card {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 400px; margin: 20px auto; }}
                img {{ width: 100%; border-radius: 10px; margin-top: 15px; }}
                .btn {{ background: #1b5e20; color: white; padding: 12px; border: none; border-radius: 8px; width: 100%; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2 style="color: #1b5e20;">👓 Vision-Link AI</h2>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <p style="font-size: 20px; font-weight: bold; color: #333;">"{fada_da_baki}"</p>
                
                <audio id="myAudio" autoplay style="width: 100%; margin-top: 10px;">
                    <source src="data:audio/mp3;base64,{audio_encoded}" type="audio/mp3">
                </audio>
                
                <button class="btn" onclick="document.getElementById('myAudio').play()">📢 SAKE JIN TURANCI/HAUSA</button>
                <br><br>
                <p style="font-size: 12px; color: #666;">Hoton da aka duba:</p>
                <img src="data:image/jpeg;base64,{hoto_encoded}" />
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h3>An samu matsala: {str(e)}</h3>")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
               
