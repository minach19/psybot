from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textblob import TextBlob
import cv2
import numpy as np
import base64
import os
from datetime import datetime
import random
import re

app = Flask(__name__)
CORS(app)

# Folder to save images temporarily
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Extended database of positive and negative words
POSITIVE_WORDS = [
    # Basic positive emotions
    'happy', 'joy', 'excited', 'amazing', 'wonderful', 'fantastic', 'great', 'excellent', 'awesome', 'brilliant',
    'love', 'beautiful', 'perfect', 'incredible', 'outstanding', 'superb', 'marvelous', 'terrific', 'fabulous',
    'delighted', 'thrilled', 'ecstatic', 'elated', 'euphoric', 'blissful', 'content', 'satisfied', 'pleased',
    
    # Achievement and success
    'success', 'win', 'victory', 'achieve', 'accomplish', 'complete', 'finish', 'progress', 'improve', 'advance',
    'excel', 'triumph', 'conquer', 'overcome', 'master', 'skilled', 'talented', 'capable', 'competent', 'confident',
    
    # Relationships and social
    'friend', 'friendship', 'bond', 'connect', 'together', 'unite', 'support', 'care', 'help', 'kindness',
    'compassion', 'empathy', 'understanding', 'trust', 'loyalty', 'appreciation', 'gratitude', 'thankful',
    
    # Energy and motivation
    'energy', 'motivated', 'inspired', 'determined', 'focused', 'productive', 'creative', 'innovative', 'fresh',
    'vibrant', 'dynamic', 'enthusiastic', 'passionate', 'driven', 'ambitious', 'optimistic', 'hopeful',
    
    # Peace and calm
    'peaceful', 'calm', 'serene', 'tranquil', 'relaxed', 'comfortable', 'safe', 'secure', 'stable', 'balanced',
    'harmony', 'zen', 'mindful', 'present', 'centered', 'grounded', 'patient', 'gentle', 'kind',
    
    # Growth and learning
    'learn', 'grow', 'develop', 'evolve', 'transform', 'change', 'adapt', 'flexible', 'open', 'curious',
    'explore', 'discover', 'adventure', 'journey', 'experience', 'knowledge', 'wisdom', 'insight', 'clarity',
    
    # Health and wellness
    'healthy', 'strong', 'fit', 'wellness', 'vitality', 'energetic', 'refreshed', 'renewed', 'revitalized',
    'healing', 'recovery', 'better', 'improved', 'restored', 'rejuvenated', 'invigorated'
]

NEGATIVE_WORDS = [
    # Basic negative emotions
    'sad', 'depressed', 'unhappy', 'miserable', 'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate',
    'angry', 'furious', 'mad', 'rage', 'irritated', 'annoyed', 'frustrated', 'upset', 'disturbed', 'agitated',
    'worried', 'anxious', 'nervous', 'scared', 'afraid', 'fearful', 'terrified', 'panic', 'stress', 'overwhelmed',
    
    # Failure and defeat
    'fail', 'failure', 'lose', 'loss', 'defeat', 'beaten', 'unsuccessful', 'wrong', 'mistake', 'error',
    'disappointment', 'disappointed', 'let down', 'betrayed', 'abandoned', 'rejected', 'ignored', 'excluded',
    
    # Pain and suffering
    'pain', 'hurt', 'suffering', 'agony', 'torture', 'ache', 'sore', 'injury', 'wound', 'damage',
    'broken', 'shattered', 'destroyed', 'ruined', 'devastated', 'crushed', 'defeated', 'hopeless',
    
    # Isolation and loneliness
    'lonely', 'alone', 'isolated', 'abandoned', 'forgotten', 'neglected', 'unwanted', 'unloved', 'empty',
    'void', 'hollow', 'meaningless', 'purposeless', 'lost', 'confused', 'disconnected', 'withdrawn',
    
    # Exhaustion and fatigue
    'tired', 'exhausted', 'drained', 'depleted', 'weary', 'fatigued', 'worn out', 'burned out', 'stressed',
    'overworked', 'overwhelmed', 'pressured', 'burdened', 'heavy', 'sluggish', 'lethargic', 'weak',
    
    # Doubt and insecurity
    'doubt', 'uncertain', 'insecure', 'vulnerable', 'weak', 'inadequate', 'insufficient', 'incompetent',
    'worthless', 'useless', 'hopeless', 'helpless', 'powerless', 'stuck', 'trapped', 'limited',
    
    # Negative thoughts
    'negative', 'pessimistic', 'cynical', 'bitter', 'resentful', 'jealous', 'envious', 'guilty', 'ashamed',
    'embarrassed', 'humiliated', 'regret', 'remorse', 'blame', 'criticize', 'judge', 'harsh'
]

MOOD_ADVICE = {
    'positive': [
        "🌟 Your positive energy is wonderful! Keep spreading those good vibes and consider sharing your happiness with others around you.",
        "✨ You're radiating positivity! This is a great time to tackle new challenges or help someone who might need encouragement.",
        "🎉 Your upbeat mood is contagious! Consider journaling about what's making you happy to remember this feeling later.",
        "🌈 You're in a fantastic headspace! Use this energy to work on goals that matter to you or connect with loved ones.",
        "💫 Your positive outlook is a gift! Consider practicing gratitude meditation to maintain this beautiful energy."
    ],
    'negative': [
        "🫂 I understand you're going through a tough time. Remember that it's okay to feel this way, and these feelings will pass.",
        "💙 Your emotions are valid. Try taking 5 deep breaths, going for a short walk, or listening to calming music.",
        "🌱 Difficult emotions are part of growth. Consider reaching out to a friend, family member, or counselor for support.",
        "🔮 This challenging moment is temporary. Try engaging in a self-care activity like a warm bath, tea, or gentle stretching.",
        "🌸 Be gentle with yourself. Consider writing down your thoughts, practicing mindfulness, or doing something creative to process these feelings.",
        "💗 You're stronger than you know. Try focusing on one small positive thing you can do for yourself right now.",
        "🌟 Every storm passes. Consider calling someone you trust, watching something uplifting, or spending time in nature if possible.",
        "🦋 Healing takes time. Try progressive muscle relaxation, meditation apps, or gentle yoga to help ease your mind."
    ],
    'neutral': [
        "🌿 You seem balanced today. This is a great time for reflection, planning, or trying something new and gentle.",
        "⚖️ Your steady mood is a strength. Consider using this calm energy to organize your thoughts or space.",
        "🍃 You're in a peaceful state. Maybe explore a new hobby, read something inspiring, or have a meaningful conversation.",
        "🌊 Your balanced energy is perfect for mindful activities like meditation, journaling, or taking a nature walk.",
        "🎯 You seem centered today. This is an ideal time to set intentions or work on personal development goals."
    ]
}

WELLNESS_TIPS = [
    "💧 Stay hydrated! Drinking water can improve your mood and energy levels.",
    "🌞 Try to get some sunlight today - it naturally boosts serotonin production.",
    "🚶‍♀️ A 10-minute walk can significantly improve your mental state.",
    "🧘‍♂️ Take 3 minutes to practice deep breathing - inhale for 4, hold for 4, exhale for 6.",
    "📱 Consider taking a break from social media if you're feeling overwhelmed.",
    "🎵 Listen to music that matches or improves your current mood.",
    "📖 Reading for just 10 minutes can reduce stress levels by up to 68%.",
    "🌱 Connect with nature, even if it's just looking at plants or the sky.",
    "💪 Gentle stretching can release physical tension that affects your mood.",
    "🎨 Express yourself creatively - draw, write, or make something with your hands."
]

def analyze_sentiment_advanced(text):
    """Advanced sentiment analysis with extended word database"""
    text_lower = text.lower()
    
    # Remove punctuation and split into words
    words = re.findall(r'\b\w+\b', text_lower)
    
    positive_count = sum(1 for word in words if word in POSITIVE_WORDS)
    negative_count = sum(1 for word in words if word in NEGATIVE_WORDS)
    
    # Use TextBlob for additional analysis
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    # Combine rule-based and TextBlob analysis
    if positive_count > negative_count or polarity > 0.2:
        mood = "positive"
        confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1 + polarity * 0.3)
    elif negative_count > positive_count or polarity < -0.2:
        mood = "negative"
        confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1 + abs(polarity) * 0.3)
    else:
        mood = "neutral"
        confidence = 0.6 + abs(polarity) * 0.2
    
    # Get personalized advice
    advice = random.choice(MOOD_ADVICE[mood])
    if mood == 'neutral' or confidence < 0.7:
        advice += "\\n\\n" + random.choice(WELLNESS_TIPS)
    
    return {
        "mood": mood,
        "polarity": polarity,
        "confidence": max(0.1, min(0.95, confidence)),
        "positive_words": positive_count,
        "negative_words": negative_count,
        "advice": advice,
        "wellness_tip": random.choice(WELLNESS_TIPS)
    }

def detect_emotion_from_face():
    """Detect emotion based on facial analysis (simulated with enhanced feedback)"""
    emotions = [
        {"mood": "Happy", "advice": "🌟 Your smile is beautiful! Keep spreading joy and consider sharing this happiness with others."},
        {"mood": "Calm", "advice": "😌 You look peaceful and centered. This is a great time for reflection or meditation."},
        {"mood": "Focused", "advice": "🎯 You appear concentrated and determined. Use this focus to tackle important tasks."},
        {"mood": "Tired", "advice": "😴 You seem a bit tired. Consider taking a break, staying hydrated, or getting some rest."},
        {"mood": "Thoughtful", "advice": "🤔 You look contemplative. This is perfect for journaling or deep thinking."},
        {"mood": "Relaxed", "advice": "🧘‍♀️ You appear relaxed and at ease. Maintain this state with some gentle activities."}
    ]
    return random.choice(emotions)

def analyze_face(image_data):
    """Analyze image to detect facial emotions"""
    try:
        # Convert base64 image to numpy array
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Load face classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return {
                "face_detected": False,
                "message": "No face detected. Please ensure you're clearly visible in good lighting.",
                "advice": "💡 Try adjusting your position or lighting for better detection. Good lighting makes a big difference!"
            }
        
        # Save image for debugging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{UPLOAD_FOLDER}/face_{timestamp}.jpg"
        cv2.imwrite(filename, img)
        
        # Get emotion analysis
        emotion_result = detect_emotion_from_face()
        
        return {
            "face_detected": True,
            "face_count": len(faces),
            "message": f"{len(faces)} face(s) detected successfully!",
            "mood": emotion_result["mood"],
            "advice": emotion_result["advice"],
            "timestamp": timestamp
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Error during image analysis. Please try again.",
            "advice": "🔧 Technical issue occurred. Please check your camera permissions and try again."
        }

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Endpoint for text analysis"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    result = analyze_sentiment_advanced(data['text'])
    return jsonify(result)

@app.route('/analyze/image', methods=['POST'])
def analyze_image():
    """Endpoint for image analysis"""
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400
    
    result = analyze_face(data['image'])
    return jsonify(result)

@app.route('/analyze/mood', methods=['POST'])
def analyze_mood():
    """Specific endpoint for camera-based mood analysis"""
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400
    
    result = analyze_face(data['image'])
    return jsonify(result)

@app.route('/analyze/combined', methods=['POST'])
def analyze_combined():
    """Endpoint for combined text + image analysis"""
    data = request.json
    if not data or 'text' not in data or 'image' not in data:
        return jsonify({"error": "Incomplete data"}), 400
    
    text_analysis = analyze_sentiment_advanced(data['text'])
    image_analysis = analyze_face(data['image'])
    
    # Combine results
    combined_result = {
        "text_analysis": text_analysis,
        "image_analysis": image_analysis,
        "combined_advice": f"{text_analysis['advice']}\\n\\n{image_analysis.get('advice', '')}",
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(combined_result)

@app.route('/wellness-tip', methods=['GET'])
def get_wellness_tip():
    """Get a random wellness tip"""
    return jsonify({
        "tip": random.choice(WELLNESS_TIPS),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🤖 PsyBot AI Wellness Coach starting...")
    print("📊 Database loaded with:")
    print(f"   • {len(POSITIVE_WORDS)} positive keywords")
    print(f"   • {len(NEGATIVE_WORDS)} negative keywords") 
    print(f"   • {sum(len(advice) for advice in MOOD_ADVICE.values())} personalized advice messages")
    print(f"   • {len(WELLNESS_TIPS)} wellness tips")
    print("🌐 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)
