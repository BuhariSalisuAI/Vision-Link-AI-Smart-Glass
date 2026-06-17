# config.py
# Vision-Link AI Smart Glass - Configuration File
# Author: Buhari Salisu
# Date: 2026-06-17

import os

# ==================== AI MODEL PATHS ====================
MODEL_PATHS = {
    'object_detection': 'app/models/object_detection.h5',
    'ocr': 'app/models/ocr_model.pb',
    'face_recognition': 'app/models/face_recognition.pkl',
}

# ==================== AUDIO SETTINGS ====================
AUDIO_SETTINGS = {
    'sample_rate': 16000,
    'chunk_size': 1024,
    'channels': 1,
    'language': 'ha',  # Hausa language code
    'volume': 0.8,
    'speech_rate': 150,  # Words per minute
}

# ==================== CAMERA SETTINGS ====================
CAMERA_SETTINGS = {
    'resolution': (640, 480),
    'fps': 30,
    'brightness': 50,
    'contrast': 50,
}

# ==================== GPS SETTINGS ====================
GPS_SETTINGS = {
    'port': '/dev/ttyUSB0',  # Raspberry Pi GPS port
    'baudrate': 9600,
    'timeout': 1,
}

# ==================== API KEYS (Keep Secret!) ====================
# NOTE: Replace with your actual API keys
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid_here')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token_here')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'whatsapp:+14155238886')

# Google Maps API (for navigation)
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'your_google_maps_api_key')

# ==================== WHATSAPP SETTINGS ====================
WHATSAPP_SETTINGS = {
    'enabled': True,
    'emergency_contact': '+234XXXXXXXXXX',  # Replace with real number
    'webhook_url': 'https://your-domain.com/whatsapp',
}

# ==================== BUTTON MAPPINGS ====================
BUTTON_ACTIONS = {
    'single_press': 'read_text',      # OCR
    'double_press': 'detect_objects',  # Object Detection
    'long_press': 'emergency_call',    # Call/WhatsApp emergency
    'triple_press': 'navigation',    # GPS navigation
}

# ==================== HAUSA PHRASES ====================
HAUSA_PHRASES = {
    'greeting': 'Barka da rana! Vision-Link AI tana shirye.',
    'ready': 'Na shirya. Ina jira umarnin ku.',
    'object_detected': 'Na gano {object} a gaban ku.',
    'no_object': 'Babu abu a gaban ku.',
    'reading': 'Ina karatu: {text}',
    'no_text': 'Babu rubutu da na iya karatu.',
    'turn_left': 'Koma hagu.',
    'turn_right': 'Koma dama.',
    'straight': 'Tafi kai tsaye.',
    'stop': 'Tsaya.',
    'emergency_sent': 'An aika saƙon gaggawa.',
    'goodbye': 'Sai an jima.',
}

# ==================== DEBUG MODE ====================
DEBUG = True
LOG_FILE = 'logs/vision_link.log'
