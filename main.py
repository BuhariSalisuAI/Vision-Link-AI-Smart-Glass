from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
import base64
import urllib.request
import os
import uvicorn

app = FastAPI(title="Vision-Link AI Smart Glasses", version="0.5.0")

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
    html_home = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vision-Link AI Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f6f9; margin: 0; padding: 20px; }
            .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 400px; margin: 40px auto; }
            .btn { background: #1b5e20; color: white; padding: 12px; border: none; border-radius: 8px; width: 100%; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 15px; }
            input[type="file"] { margin-top: 15px; width: 100%; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="color: #1b5e20;">👓 Vision-Link AI</h2>
            <p style="color: #666;">Zaɓi hoton mota, mutum, ko kujera don duba basirar AI</p>
            <form action="/abubuwa" method="post" enctype="multipart/form-data">
                <input type="file" name="hoto" accept="image/*" required>
                <button type="submit" class="btn">🚀 FARA GANE ABUTU</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html_home

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

        # Kamus na fassarar Hausa da Turanci
        fassara_dict = {
            "car": {"ha": "mota", "en": "Car"},
            "person": {"ha": "mutum", "en": "Person"},
            "bus": {"ha": "babban mota", "en": "Bus"},
            "motorbike": {"ha": "babur", "en": "Motorbike"},
            "bicycle": {"ha": "keke", "en": "Bicycle"},
            "chair": {"ha": "kujera", "en": "Chair"},
            "diningtable": {"ha": "tebur", "en": "Table"},
            "bottle": {"ha": "gora", "en": "Bottle"}
        }

        if not abubuwan_da_aka_gani:
            fada_da_baki = "Malam, ban gano kowane cikas ba a gabanka."
            rubutun_shafi = "Babu abin da aka gano / No objects detected"
        else:
            hausa_list = []
            rubutu_list = []
            
            for obj in abubuwan_da_aka_gani:
                if obj in fassara_dict:
                    hausa_list.append(fassara_dict[obj]["ha"])
                    rubutu_list.append(f"{fassara_dict[obj]['en']} ({fassara_dict[obj]['ha']})")
                else:
                    hausa_list.append(obj)
                    rubutu_list.append(obj)
            
            gajeren_hausa = " da ".join(hausa_list)
            rubutun_shafi = ", ".join(rubutu_list)
            
            # Wannan ita ce ainihin jimlar da kake so Buhari abokina
            fada_da_baki = f"Malam, na gano {gajeren_hausa} a gabanka. Ka koma ɗayan hannun saboda matsalar idanunka."

        # Samar da muryar Hausa ta gTTS
        from gtts import gTTS
        fayil_sauti = "sauti.mp3"
        tts = gTTS(text=fada_da_baki, lang='ha', slow=False)
        tts.save(fayil_sauti)

        with open(fayil_sauti, "rb") as f:
            audio_encoded = base64.b64encode(f.read()).decode("utf-8")

        _, encoded_img = cv2.imencode('.jpg', img)
        hoto_encoded = base64.b64encode(encoded_img).decode('utf-8')

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vision-Link AI Result</title>
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
                
                <p style="font-size: 24px; font-weight: bold; color: #1b5e20; margin-bottom: 5px;">{rubutun_shafi}</p>
                <p style="font-size: 16px; color: #333; font-weight: 500; padding: 0 10px;">"{fada_da_baki}"</p>
                
                <audio autoplay id="player" style="width:100%; margin-top:10px;" controls>
                    <source src="data:audio/mp3;base64,{audio_encoded}" type="audio/mp3">
                </audio>
                
                <button class="btn" onclick="document.getElementById('player').play()">📢 SAKE JIN MURYAR</button>
                <br><br>
                <img src="data:image/jpeg;base64,{hoto_encoded}" />
                <br><br>
                <a href="/" style="color: #1b5e20; text-decoration: none; font-weight: bold;">← Koma Baya</a>
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
               
