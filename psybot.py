from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textblob import TextBlob
import cv2
import numpy as np
import base64
import os
from datetime import datetime
import tensorflow as tf
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Dossier pour sauvegarder temporairement les images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialiser le modèle de sentiment
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    """Analyse le sentiment du texte avec BERT"""
    try:
        result = sentiment_analyzer(text)[0]
        score = result['score']
        label = result['label']
        
        # Convertir le label en humeur
        if '5' in label or '4' in label:
            mood = "positif"
        elif '1' in label or '2' in label:
            mood = "négatif"
        else:
            mood = "neutre"
        
        return {
            "mood": mood,
            "polarity": float(label.split()[0]) / 5,  # Normaliser entre 0 et 1
            "confidence": score
        }
    except Exception as e:
        # Fallback sur TextBlob si BERT échoue
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
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
        
        # Analyser chaque visage
        face_analyses = []
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            # Ici, on pourrait ajouter l'analyse d'émotion avec un modèle ML
            face_analyses.append({
                "position": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                "confidence": 1.0  # À remplacer par la vraie confiance du modèle
            })
        
        return {
            "face_detected": True,
            "face_count": len(faces),
            "faces": face_analyses,
            "message": f"{len(faces)} visage(s) détecté(s)"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Erreur lors de l'analyse de l'image"
        }

@app.route('/')
def home():
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