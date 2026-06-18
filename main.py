from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
from PIL import Image
import io
import base64

app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.2.0")

# Abubuwan da AI dinmu zai iya ganewa (MobileNet-SSD Classes)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

@app.get("/")
async def home():
    return {"sako": "Sabar Vision-Link AI tana aiki lafiya! 🚀"}

@app.post("/abubuwa", summary="Gane Abubuwa da Kyamara")
async def gane_abubuwa(hoto: UploadFile = File(...)):
    try:
        # 1. Karanta hoton da aka turo daga kyamara
        contents = await hoto.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        h, w = img.shape[:2]

        # 2. Dauko pre-trained AI Model daga Intanet (MobileNet-SSD)
        prototxt_url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt"
        model_url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/mobilenet_iter_73000.caffemodel"
        
        # Karanta model din ta amfani da OpenCV OpenCV DNN
        net = cv2.dnn.readNetFromCaffe(
            cv2.utils.findFileOrKeep(prototxt_url), 
            cv2.utils.findFileOrKeep(model_url)
        )

        # 3. Sanya hoton a cikin tsarin da AI zai gane (Blob)
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        abubuwan_da_aka_gani = []

        # 4. Bincika abubuwan da AI din ya gano a cikin hoton
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Idan AI ya tabbata sama da 50%
                class_id = int(detections[0, 0, i, 1])
                object_name = CLASSES[class_id]
                if object_name not in abubuwan_da_aka_gani:
                    abubuwan_da_aka_gani.append(object_name)

        # 5. Idan AI bai gano komai ba, mu bar shi da babu
        if not abubuwan_da_aka_gani:
            fada_da_baki = "Ban gano komai ba a gabanka"
            rubutu_shafi = "Babu abin da aka gano"
        else:
            # Hada sunayen abubuwan da aka gani
            gajeren_rubutu = ", ".join(abubuwan_da_aka_gani)
            fada_da_baki = f"Ina gani {gajeren_rubutu}"
            rubutu_shafi = f"An gano: {gajeren_rubutu}"

        # 6. Juye sakamakon zuwa Muryar Google TTS (Hausa)
        from gtts import gTTS
        fayil_sauti = "gane_abubuwa.mp3"
        tts = gTTS(text=fada_da_baki, lang='ha', slow=False)
        tts.save(fayil_sauti)

        with open(fayil_sauti, "rb") as f:
            audio_encoded = base64.b64encode(f.read()).decode("utf-8")

        # 7. Dawo da kyakkyawan shafin da zai kunna sauti kai tsaye
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
        <body style="margin:0; padding:40px 20px; font-family:Arial; text-align:center; background:#f4f6f9;">
            <div style="background:white; padding:30px; border-radius:15px; box-shadow:0 4px 15px rgba(0,0,0,0.1); max-width:400px; margin:0 auto;">
                <h2 style="color:#1b5e20;">👓 Vision-Link AI Glasses</h2>
                <p style="color:#666;">Object Detection Audio</p>
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
        return HTMLResponse(content=f"<h3>An samu matsala wajen gane abu: {str(e)}</h3>")
