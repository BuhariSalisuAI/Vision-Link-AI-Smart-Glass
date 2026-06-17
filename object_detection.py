import cv2
import tensorflow as tf

def detect_objects():
    # Loda pre-trained model
    model = tf.keras.models.load_model('app/models/object_detection.h5')
    # Gano abubuwa daga kyamara
    # ...
    return "mutum, mota, bango"
