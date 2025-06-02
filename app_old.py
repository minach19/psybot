from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textblob import TextBlob
import cv2
import numpy as np
import base64
import os
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Dossier pour sauvegarder temporairement les images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def analyze_sentiment(text):
    """Analyse le sentiment du texte avec TextBlob"""
    analysis = TextBlob(text)
    # La polarité est entre -1 (négatif) et 1 (positif)
    polarity = analysis.sentiment.polarity
    
    # Déterminer l'humeur basée sur la polarité
    if polarity > 0.3:
        mood = "positif"
    elif polarity < -0.3:
        mood = "négatif"
    else:
        mood = "neutre"
    
    return {
        "mood": mood,
        "polarity": polarity,
        "confidence": abs(polarity)
    }

def detect_emotion_from_face():
    """Détecte l'émotion basée sur l'analyse faciale (simulée)"""
    emotions = ["Heureux", "Triste", "Neutre", "Surpris", "En colère", "Détendu"]
    return random.choice(emotions)

def analyze_face(image_data):
    """Analyse l'image pour détecter les émotions faciales"""
    try:
        # Convertir l'image base64 en array numpy
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Charger le classificateur de visage
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Détecter les visages
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return {
                "face_detected": False,
                "message": "Aucun visage détecté"
            }
        
        # Sauvegarder l'image pour debug
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{UPLOAD_FOLDER}/face_{timestamp}.jpg"
        cv2.imwrite(filename, img)
        
        return {
            "face_detected": True,
            "face_count": len(faces),
            "message": f"{len(faces)} visage(s) détecté(s)",
            "mood": detect_emotion_from_face()
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Erreur lors de l'analyse de l'image"
        }

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Endpoint pour l'analyse de texte"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Aucun texte fourni"}), 400
    
    result = analyze_sentiment(data['text'])
    return jsonify(result)

@app.route('/analyze/image', methods=['POST'])
def analyze_image():
    """Endpoint pour l'analyse d'image"""
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "Aucune image fournie"}), 400
    
    result = analyze_face(data['image'])
    return jsonify(result)

@app.route('/analyze/mood', methods=['POST'])
def analyze_mood():
    """Endpoint spécifique pour l'analyse d'humeur via caméra"""
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "Aucune image fournie"}), 400
    
    result = analyze_face(data['image'])
    return jsonify(result)

@app.route('/analyze/combined', methods=['POST'])
def analyze_combined():
    """Endpoint pour l'analyse combinée texte + image"""
    data = request.json
    if not data or 'text' not in data or 'image' not in data:
        return jsonify({"error": "Données incomplètes"}), 400
    
    text_analysis = analyze_sentiment(data['text'])
    image_analysis = analyze_face(data['image'])
    
    # Combiner les résultats
    combined_result = {
        "text_analysis": text_analysis,
        "image_analysis": image_analysis,
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(combined_result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)