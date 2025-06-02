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
import requests

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
    'healing', 'recovery', 'better', 'improved', 'restored', 'rejuvenated', 'invigorated',
    
    # Additional positive words
    'blessed', 'grateful', 'appreciate', 'cherish', 'treasure', 'admire', 'respect', 'honor', 'value',
    'celebrate', 'rejoice', 'cheer', 'applaud', 'praise', 'compliment', 'encourage', 'inspire', 'motivate',
    'uplifting', 'cheerful', 'joyful', 'gleeful', 'merry', 'jolly', 'bright', 'radiant', 'glowing',
    'sparkling', 'shining', 'brilliant', 'magnificent', 'splendid', 'gorgeous', 'stunning', 'breathtaking',
    'remarkable', 'exceptional', 'extraordinary', 'phenomenal', 'spectacular', 'impressive', 'admirable',
    'worthy', 'deserving', 'special', 'unique', 'precious', 'valuable', 'important', 'meaningful',
    'fulfilling', 'rewarding', 'satisfying', 'gratifying', 'pleasant', 'enjoyable', 'delightful', 'charming'
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
    'embarrassed', 'humiliated', 'regret', 'remorse', 'blame', 'criticize', 'judge', 'harsh',
    
    # Additional negative words
    'disgusted', 'revolted', 'sickened', 'appalled', 'horrified', 'shocked', 'stunned', 'bewildered',
    'confused', 'perplexed', 'puzzled', 'baffled', 'troubled', 'disturbed', 'unsettled', 'uneasy',
    'uncomfortable', 'awkward', 'embarrassing', 'shameful', 'disgraceful', 'humiliating', 'degrading',
    'offensive', 'insulting', 'hurtful', 'harmful', 'damaging', 'destructive', 'toxic', 'poisonous',
    'threatening', 'dangerous', 'risky', 'unsafe', 'precarious', 'unstable', 'chaotic', 'disorganized',
    'messy', 'cluttered', 'overwhelming', 'suffocating', 'stifling', 'oppressive', 'restrictive',
    'limiting', 'constraining', 'binding', 'trapped', 'imprisoned', 'confined', 'restricted', 'blocked'
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
        "🦋 Healing takes time. Try progressive muscle relaxation, meditation apps, or gentle yoga to help ease your mind.",
        "🌈 Remember: you've overcome challenges before, and you can do it again. Consider what has helped you in the past.",
        "💪 Your feelings are temporary, but your strength is permanent. Try the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
        "🕊️ Practice self-compassion. Speak to yourself as you would to a dear friend. You deserve kindness, especially from yourself.",
        "🌊 Emotions are like waves - they rise, peak, and then naturally fall. Let this feeling flow through you without resistance."
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

# 🧩 Nouveaux éléments pour l'avatar et le bien-être
BREATHING_EXERCISES = [
    {
        "name": "Respiration 4-7-8",
        "description": "Inspirez 4 secondes, retenez 7 secondes, expirez 8 secondes",
        "duration": 4,
        "instructions": [
            "Placez votre langue contre le palais",
            "Inspirez par le nez pendant 4 secondes",
            "Retenez votre souffle pendant 7 secondes",
            "Expirez complètement par la bouche pendant 8 secondes"
        ]
    },
    {
        "name": "Respiration profonde",
        "description": "Respiration diaphragmatique pour la relaxation",
        "duration": 5,
        "instructions": [
            "Placez une main sur votre poitrine, une sur votre ventre",
            "Inspirez lentement par le nez",
            "Sentez votre ventre se gonfler",
            "Expirez doucement par la bouche"
        ]
    },
    {
        "name": "Respiration en carré",
        "description": "Technique de respiration rythmée pour le calme",
        "duration": 4,
        "instructions": [
            "Inspirez pendant 4 temps",
            "Retenez pendant 4 temps",
            "Expirez pendant 4 temps",
            "Pausez pendant 4 temps"
        ]
    }
]

STRETCH_EXERCISES = [
    {
        "name": "Étirement du cou",
        "description": "Soulage les tensions cervicales",
        "duration": 30,
        "instructions": [
            "Inclinez doucement la tête vers la droite",
            "Tenez 15 secondes",
            "Répétez de l'autre côté",
            "Tournez lentement la tête en cercle"
        ]
    },
    {
        "name": "Étirement des épaules",
        "description": "Relâche les tensions des épaules",
        "duration": 45,
        "instructions": [
            "Roulez les épaules vers l'arrière 10 fois",
            "Levez les bras au-dessus de la tête",
            "Étirez-vous vers le haut",
            "Relâchez lentement"
        ]
    },
    {
        "name": "Étirement du dos",
        "description": "Étirement pour le bas du dos",
        "duration": 60,
        "instructions": [
            "Asseyez-vous au bord de votre chaise",
            "Penchez-vous doucement vers l'avant",
            "Laissez vos bras pendre",
            "Redressez-vous lentement"
        ]
    }
]

MOTIVATIONAL_MESSAGES = [
    "🌟 Vous êtes capable de plus que vous ne l'imaginez !",
    "💪 Chaque petit pas compte dans votre parcours de bien-être.",
    "🌱 La croissance personnelle demande du temps, soyez patient avec vous-même.",
    "✨ Votre santé mentale mérite autant d'attention que votre santé physique.",
    "🦋 Les changements positifs commencent par de petites actions quotidiennes.",
    "🌈 Après chaque tempête vient un arc-en-ciel.",
    "💚 Prenez soin de vous, vous le méritez.",
    "🎯 Concentrez-vous sur le progrès, pas sur la perfection.",
    "🌸 La mindfulness transforme l'ordinaire en extraordinaire.",
    "⭐ Vous avez déjà surmonté des défis, vous pouvez le refaire !"
]

AVATAR_PERSONALITIES = {
    "zen": {
        "emoji": "🧘‍♀️",
        "messages": [
            "Prenons un moment pour respirer ensemble...",
            "La paix intérieure commence par une respiration profonde.",
            "Votre bien-être est ma priorité aujourd'hui."
        ]
    },
    "energetic": {
        "emoji": "💃",
        "messages": [
            "C'est le moment de bouger et de s'étirer !",
            "L'énergie positive commence par le mouvement !",
            "Allez, on fait quelques étirements ensemble !"
        ]
    },
    "wise": {
        "emoji": "🦉",
        "messages": [
            "Laissez-moi partager une pensée inspirante avec vous...",
            "La sagesse vient de l'écoute de soi.",
            "Chaque jour est une opportunité d'apprendre."
        ]
    }
}

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

# 🧩 Nouveaux endpoints pour l'avatar et le bien-être
@app.route('/avatar/breathing-exercise', methods=['GET'])
def get_breathing_exercise():
    """Get a random breathing exercise"""
    exercise = random.choice(BREATHING_EXERCISES)
    return jsonify({
        "exercise": exercise,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/avatar/stretch-exercise', methods=['GET'])
def get_stretch_exercise():
    """Get a random stretch exercise"""
    exercise = random.choice(STRETCH_EXERCISES)
    return jsonify({
        "exercise": exercise,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/avatar/motivation', methods=['GET'])
def get_motivation():
    """Get a motivational message"""
    message = random.choice(MOTIVATIONAL_MESSAGES)
    return jsonify({
        "message": message,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/avatar/personality', methods=['POST'])
def set_avatar_personality():
    """Set avatar personality and get personalized messages"""
    data = request.json
    personality_type = data.get('personality', 'zen')
    
    if personality_type in AVATAR_PERSONALITIES:
        personality = AVATAR_PERSONALITIES[personality_type]
        message = random.choice(personality['messages'])
        
        return jsonify({
            "personality": personality_type,
            "emoji": personality['emoji'],
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    else:
        return jsonify({"error": "Invalid personality type"}), 400

@app.route('/avatar/speak', methods=['POST'])
def avatar_speak():
    """Generate personalized avatar message based on mood"""
    data = request.json
    mood = data.get('mood', 'neutral')
    user_name = data.get('name', 'ami')
    
    # Messages personnalisés selon l'humeur
    mood_messages = {
        'positive': [
            f"C'est fantastique {user_name} ! Votre énergie positive rayonne ! ✨",
            f"Vous semblez en pleine forme {user_name} ! Continuez sur cette lancée ! 🌟",
            f"Votre bonne humeur est contagieuse {user_name} ! 😊"
        ],
        'negative': [
            f"Je sens que ça va moins bien {user_name}. Voulez-vous essayer un exercice de respiration ? 🫂",
            f"Prenons un moment ensemble {user_name}. Vous n'êtes pas seul(e). 💙",
            f"Il est normal d'avoir des hauts et des bas {user_name}. Que diriez-vous d'un peu de relaxation ? 🌸"
        ],
        'neutral': [
            f"Comment puis-je vous aider aujourd'hui {user_name} ? 🤗",
            f"Prêt(e) pour un moment de bien-être {user_name} ? 🧘‍♀️",
            f"Que diriez-vous d'une petite pause détente {user_name} ? ✨"
        ]
    }
    
    message = random.choice(mood_messages.get(mood, mood_messages['neutral']))
    
    return jsonify({
        "message": message,
        "mood": mood,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/exercises/all', methods=['GET'])
def get_all_exercises():
    """Get all available exercises"""
    return jsonify({
        "breathing_exercises": BREATHING_EXERCISES,
        "stretch_exercises": STRETCH_EXERCISES,
        "motivational_messages": MOTIVATIONAL_MESSAGES,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/proxy/save_avatar', methods=['POST', 'GET', 'OPTIONS'])
def proxy_save_avatar():
    print("\n=== Proxy Request Details ===")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers:")
    for header, value in request.headers.items():
        print(f"  {header}: {value}")
    print(f"Data: {request.get_data()}")
    print(f"Cookies: {request.cookies}")
    print("===========================\n")
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        print("Handling OPTIONS request")
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '86400'
        print("OPTIONS response headers:", dict(response.headers))
        return response
        
    try:
        # Prepare headers for PHP request
        headers = {
            'Content-Type': request.headers.get('Content-Type', 'application/json'),
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'http://localhost:5000'
        }
        
        print("\n=== PHP Request Details ===")
        print(f"URL: http://localhost/psybot/save_avatar.php")
        print(f"Method: {request.method}")
        print(f"Headers: {headers}")
        print(f"Data: {request.get_data()}")
        print("===========================\n")
        
        # Forward the request to the PHP endpoint
        response = requests.request(
            method=request.method,
            url='http://localhost/psybot/save_avatar.php',
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True
        )
        
        print("\n=== PHP Response Details ===")
        print(f"Status Code: {response.status_code}")
        print(f"Headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        print(f"Content: {response.content}")
        print("===========================\n")
        
        # Create Flask response
        flask_response = app.make_response(response.content)
        flask_response.status_code = response.status_code
        
        # Set CORS headers
        flask_response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
        flask_response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        flask_response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        flask_response.headers['Access-Control-Allow-Credentials'] = 'true'
        flask_response.headers['Access-Control-Max-Age'] = '86400'
        
        # Copy other headers from PHP response
        for key, value in response.headers.items():
            if key.lower() not in ['access-control-allow-origin', 'access-control-allow-methods', 
                                 'access-control-allow-headers', 'access-control-allow-credentials',
                                 'access-control-max-age']:
                flask_response.headers[key] = value
        
        print("\n=== Final Response Headers ===")
        for header, value in flask_response.headers.items():
            print(f"  {header}: {value}")
        print("===========================\n")
        
        return flask_response
        
    except Exception as e:
        print("\n=== Proxy Error ===")
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        print("===================\n")
        
        error_response = jsonify({
            'status': 'error',
            'message': f'Proxy error: {str(e)}'
        })
        error_response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
        error_response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        error_response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        error_response.headers['Access-Control-Allow-Credentials'] = 'true'
        return error_response, 500

if __name__ == '__main__':
    print("🤖 PsyBot AI Wellness Coach starting...")
    print("📊 Database loaded with:")
    print(f"   • {len(POSITIVE_WORDS)} positive keywords")
    print(f"   • {len(NEGATIVE_WORDS)} negative keywords") 
    print(f"   • {sum(len(advice) for advice in MOOD_ADVICE.values())} personalized advice messages")
    print(f"   • {len(WELLNESS_TIPS)} wellness tips")
    print("🧩 New Avatar Features:")
    print(f"   • {len(BREATHING_EXERCISES)} breathing exercises")
    print(f"   • {len(STRETCH_EXERCISES)} stretch exercises")
    print(f"   • {len(MOTIVATIONAL_MESSAGES)} motivational messages")
    print(f"   • {len(AVATAR_PERSONALITIES)} avatar personalities")
    print("🌐 Server running on http://localhost:5000")
    print("🎯 New endpoints available:")
    print("   • /avatar/breathing-exercise - Get breathing exercises")
    print("   • /avatar/stretch-exercise - Get stretch exercises") 
    print("   • /avatar/motivation - Get motivational messages")
    print("   • /avatar/speak - Personalized avatar messages")
    print("   • /exercises/all - Get all exercises")
    app.run(debug=True, port=5000)
