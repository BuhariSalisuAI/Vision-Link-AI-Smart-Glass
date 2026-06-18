from fastapi import FastAPI
from pydantic import BaseModel

# 1. Janyo fayilolin ayyukan AI dinka
from ocr_reader import OCRReader
from navigation import NavigationSystem
# Idan kana da wani fayil na gane abubuwa (object detection), zaka iya kara shi anan gaba

# 2. Kirkirar sabar API
app = FastAPI()

# 3. Tsarin karbar bayani (misali: idan za a turo sunan gari/unguwa)
class Waje(BaseModel):
    unguwa: str

# ==========================================
# KOFOFIN API DINMU (ENDPOINTS)
# ==========================================

# Kofa ta 0: Gwajin Sabar (Don tabbatar tana raye)
@app.get("/")
def home():
    return {"message": "Vision-Link AI is Live and Running!"}

# Kofa ta 1: Karanta Rubutu (OCR)
@app.post("/karatu")
def karanta_rubutu():
    # Aikin karanta rubutu daga OCR
    text = OCRReader().read_text() 
    return {"sakamako": text, "matsayi": "An yi nasara"}

# Kofa ta 2: Bayar da Hanya (Navigation)
@app.post("/hanya")
def bada_hanya(waje: Waje):
    # Aikin nemo hanyar zuwa inda aka ambata
    directions = NavigationSystem().get_directions(waje.unguwa)
    return {"sakamako": directions, "matsayi": "An yi nasara"}

# Kofa ta 3: Gane Abubuwa (Object Detection - Misali don an gaba)
@app.post("/abubuwa")
def gane_abubuwa():
    # A nan zamu jona asalin aikin gane abubuwa idan mun shirya masa
    return {"sakamako": "Na gano Kujera, Mutum da Kwamfuta", "matsayi": "Gwajin Kofa"}
