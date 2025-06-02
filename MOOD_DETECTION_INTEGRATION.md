# Guide d'Intégration de la Détection d'Humeur avec l'Avatar PsyBot

## Introduction

Ce document technique détaille comment l'avatar personnalisable de PsyBot s'intègre avec le système de détection d'humeur en temps réel. Cette intégration permet à l'avatar de réagir de manière appropriée aux états émotionnels détectés chez l'utilisateur.

## Architecture du Système

L'intégration repose sur trois composants principaux:

1. **Système de Détection d'Humeur** - Analyse faciale via webcam
2. **Système d'Avatar** - Interface utilisateur personnalisable
3. **Système d'Intégration** - Middleware qui connecte les deux systèmes

```
┌────────────────┐      ┌────────────────────┐      ┌──────────────┐
│                │      │                    │      │              │
│  Détection     │─────▶│    Intégration     │─────▶│    Avatar    │
│  d'Humeur      │      │    (AvatarMood     │      │  (Animations │
│  (API Flask)   │◀─────│    Integration)    │◀─────│   & UI)      │
│                │      │                    │      │              │
└────────────────┘      └────────────────────┘      └──────────────┘
```

## Fichiers Clés

- `avatar-mood-integration.js` - Classe d'intégration principale
- `avatar-mood-functions.js` - Fonctions d'intégration avec l'UI
- `main.js` - Logique principale de l'application
- `avatar-customizer.js` - Système de personnalisation de l'avatar

## Flux de Données

### 1. Détection d'Humeur

Le système utilise l'API Flask pour analyser les expressions faciales:

```javascript
function captureMood() {
    // Capture image from webcam
    canvas.width = modalVideo.videoWidth;
    canvas.height = modalVideo.videoHeight;
    context.drawImage(modalVideo, 0, 0);
    
    const imageData = canvas.toDataURL('image/jpeg').split(',')[1];
    
    // Send to Flask API
    fetch('http://localhost:5000/analyze/mood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        // Process detected mood
        if (data.face_detected && data.mood) {
            window.processMoodDetection(data.mood, data.confidence || 0.8);
        }
        displayMoodResult(data);
    });
}
```

### 2. Traitement de l'Humeur Détectée

La classe `AvatarMoodIntegration` traite l'humeur détectée et détermine la réponse appropriée:

```javascript
class AvatarMoodIntegration {
    processMoodDetection(mood, confidence) {
        // Only process if confidence is above threshold
        if (confidence < 0.65) return null;
        
        // Avoid responding too frequently
        const now = Date.now();
        if ((now - this.moodResponseTimestamp) < this.moodResponseCooldown) return null;
        
        // Don't respond if mood hasn't changed
        if (mood === this.lastDetectedMood) return null;
        
        // Update state
        this.lastDetectedMood = mood;
        this.moodResponseTimestamp = now;
        
        // Return response if defined for this mood
        if (this.moodAnimations[mood]) {
            return {
                animation: this.moodAnimations[mood].animation,
                message: this.moodAnimations[mood].message,
                exerciseRecommendation: this.moodAnimations[mood].exerciseRecommendation,
                timestamp: now
            };
        }
        return null;
    }
}
```

### 3. Réponse de l'Avatar

Lorsqu'une réponse est générée, l'avatar réagit avec:

1. Une animation adaptée à l'humeur
2. Un message contextuel
3. Une recommandation d'exercice appropriée

```javascript
function setupMoodDetectionIntegration() {
    window.processMoodDetection = function(detectedMood, confidenceLevel) {
        if (!avatarMoodSystem) return;
        
        const moodResponse = avatarMoodSystem.processMoodDetection(detectedMood, confidenceLevel);
        
        if (moodResponse && moodResponse.message) {
            // Display avatar message
            avatarSpeak(moodResponse.message);
            
            // If appropriate, suggest an exercise
            if (moodResponse.exerciseRecommendation) {
                const exercise = avatarMoodSystem.getRecommendedExercise(detectedMood);
                
                // Show exercise suggestion
                setTimeout(() => {
                    addMessage(`💡 Based on your current mood, would you like to try a ${exercise.type} exercise?`, 'bot');
                    // Add exercise buttons...
                }, 2000);
            }
        }
    };
}
```

## Configuration des Réponses Émotionnelles

Les réponses de l'avatar sont configurées dans `AvatarMoodIntegration` via l'objet `moodAnimations`:

```javascript
this.moodAnimations = {
    happy: {
        animation: 'celebration',
        message: 'Your positive energy is great to see!',
        exerciseRecommendation: 'energizing_breath'
    },
    sad: {
        animation: 'empathy',
        message: 'I notice you might be feeling down. Would you like a quick mood-lifting exercise?',
        exerciseRecommendation: 'mood_lifting_breath'
    },
    // autres humeurs...
};
```

## Personnalisation des Exercices

Chaque humeur est associée à des exercices spécifiques qui peuvent être personnalisés:

```javascript
const exerciseConfigs = {
    calming_breath: {
        type: 'breathing',
        animation: '/static/animations/breathing/calming.json',
        duration: 90,
        instructions: 'Breathe in for 4, hold for 7, out for 8...'
    },
    // autres exercices...
};
```

## Intégration avec l'Interface Utilisateur

Le système utilise plusieurs méthodes pour intégrer les réponses émotionnelles à l'UI:

1. **Dialogue Contextuel** - Via la fonction `avatarSpeak`
2. **Exercices Recommandés** - Via les fonctions `startCustomBreathingExercise` et `startCustomStretchExercise`
3. **Animations Adaptées** - Via la fonction `loadLottieAnimation`

## Extensions Futures

### Possibilités d'Amélioration

1. **Historique d'Humeur Plus Détaillé**
   - Suivi temporel des changements d'humeur
   - Visualisations graphiques des tendances émotionnelles

2. **Réponses Contextualisées**
   - Adaption des réponses selon l'heure de la journée
   - Personnalisation basée sur l'historique de l'utilisateur

3. **Intelligence Artificielle**
   - Apprentissage des préférences de l'utilisateur
   - Amélioration des recommandations d'exercices par ML

## Annexe: Types d'Humeurs Détectables

| Humeur    | Description                                | Animation Associée | Exercice Recommandé   |
|-----------|--------------------------------------------|--------------------|----------------------|
| Happy     | Expression positive, sourire               | celebration        | energizing_breath    |
| Sad       | Expression négative, coins de bouche baissés | empathy          | mood_lifting_breath  |
| Angry     | Sourcils froncés, expression tendue        | calming           | calming_breath       |
| Fearful   | Regard élargi, expression d'anxiété        | supportive        | grounding_breath     |
| Neutral   | Expression neutre, pas d'émotion marquée   | neutral           | focus_breath         |
| Surprised | Sourcils relevés, bouche ouverte           | attentive         | refocus_breath       |

---

Pour toute question technique supplémentaire concernant l'intégration, veuillez consulter les fichiers source ou contacter l'équipe de développement.
