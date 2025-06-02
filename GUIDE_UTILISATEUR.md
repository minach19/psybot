# 🧘‍♀️ Guide d'Utilisation - PsyBot Avatar Interactif

## 🚀 Démarrage Rapide

### 1. Lancement de l'Application
```bash
# Démarrer le serveur
cd c:\xampp\htdocs\psybot
python app.py

# Ouvrir dans le navigateur
http://localhost:5000
```

### 2. Première Interaction avec l'Avatar
- 👀 **Localisation** : Votre avatar personnel apparaît en bas à droite de l'écran
- 🖱️ **Interaction** : Cliquez sur l'avatar pour recevoir un message personnalisé
- 💬 **Messages** : L'avatar s'adapte à votre humeur détectée et vous encourage

## 🛠️ Personnalisation de votre Avatar

### Accès aux Paramètres
1. Cliquez sur votre avatar flottant
2. Dans la bulle qui apparaît, cliquez sur **"Personnaliser"**
3. Une fenêtre de configuration s'ouvre

### Options de Personnalisation

#### 🎨 **Style d'Avatar**
Choisissez parmi 6 styles uniques :
- 🧘‍♀️ **Zen** : Pour la méditation et la relaxation
- 🤖 **Robotique** : Style technologique moderne
- 😊 **Souriant** : Visage amical et chaleureux  
- 🌟 **Étoile** : Inspirant et motivant
- 🦋 **Papillon** : Délicat et transformateur
- 🌈 **Arc-en-ciel** : Coloré et joyeux

#### 📝 **Nom Personnalisé**
- Donnez un nom unique à votre avatar
- Exemples : Maya, Alex, Luna, Aria...
- L'avatar utilisera ce nom dans ses interactions

#### ⏰ **Fréquence des Encouragements**
- **Élevée** : Messages toutes les 5 minutes
- **Moyenne** : Messages toutes les 15 minutes (recommandé)
- **Faible** : Messages toutes les 30 minutes

#### 🎯 **Préférences d'Exercices**
Activez/désactivez selon vos besoins :
- ✅ **Exercices de respiration** : Techniques de relaxation
- ✅ **Étirements** : Mouvements pour le bureau
- ✅ **Phrases motivantes** : Citations inspirantes

## 🌿 Centre de Bien-être

### Accès au Panel
- Cliquez sur le bouton **"Wellness"** dans l'interface principale
- Un panel coulissant s'ouvre sur la droite

### 🫁 Exercices de Respiration

#### Types d'Exercices Disponibles :
1. **Respiration 4-7-8**
   - Technique de relaxation profonde
   - Inspirez 4s, retenez 7s, expirez 8s
   - Idéal pour réduire le stress

2. **Respiration Profonde**
   - Respiration diaphragmatique
   - Focus sur le mouvement du ventre
   - Excellent pour la détente

3. **Respiration en Carré**
   - Technique rythmée 4-4-4-4
   - Parfait pour la concentration
   - Aide à calmer l'esprit

#### Comment Utiliser :
1. Cliquez sur **"Respiration Guidée"**
2. Lisez les instructions détaillées
3. Suivez l'animation du cercle de respiration
4. L'exercice se termine automatiquement après 10 cycles

### 🤸‍♀️ Étirements de Bureau

#### Exercices Disponibles :
1. **Étirement du Cou**
   - Soulage les tensions cervicales
   - Mouvements latéraux et circulaires
   - Durée : 30 secondes

2. **Étirement des Épaules**
   - Relâche les tensions des épaules
   - Rotation et élévation des bras
   - Durée : 45 secondes

3. **Étirement du Dos**
   - Étirement du bas du dos
   - Position assise adaptée
   - Durée : 60 secondes

#### Comment Utiliser :
1. Cliquez sur **"Étirements Bureau"**
2. Suivez les instructions visuelles
3. L'avatar vous guide avec des animations
4. Respectez le rythme indiqué

### 💬 Messages Motivationnels

#### Types de Messages :
- Citations inspirantes sur le bien-être
- Encouragements personnalisés
- Rappels de self-care
- Phrases de motivation positive

#### Comment Utiliser :
1. Cliquez sur **"Motivation"**
2. Recevez un message adapté à votre état
3. Cliquez sur **"Nouvelle Citation"** pour changer
4. L'avatar s'anime pendant la lecture

## 📱 Fonctionnalités Automatiques

### Encouragements Spontanés
- L'avatar vous parle automatiquement selon la fréquence configurée
- Les messages s'adaptent à votre humeur détectée
- Apparition naturelle et non-intrusive

### Adaptation Contextuelle
- L'avatar analyse vos interactions précédentes
- Les conseils deviennent plus personnalisés avec le temps
- Suggestions d'exercices basées sur vos préférences

### Sauvegarde Automatique
- Toutes vos préférences sont sauvegardées automatiquement
- Configuration restaurée à chaque visite
- Aucune perte de personnalisation

## 🎯 Conseils d'Utilisation Optimale

### Pour le Bien-être au Travail
1. **Matin** : Commencez par une respiration profonde
2. **Pause déjeuner** : Faites quelques étirements
3. **Après-midi** : Écoutez un message motivationnel
4. **Fin de journée** : Terminez par de la relaxation

### Intégration dans votre Routine
- Configurez les encouragements sur "Moyenne" pour commencer
- Activez toutes les préférences d'exercices initialement
- Ajustez selon vos besoins au fil du temps
- Utilisez l'avatar comme rappel de self-care

### Maximiser les Bénéfices
- Pratiquez régulièrement les exercices de respiration
- Prenez les étirements au sérieux (qualité > quantité)
- Lisez attentivement les messages motivationnels
- Personnalisez l'avatar pour créer un lien émotionnel

## 🔧 Dépannage

### L'Avatar ne Répond Pas
- Vérifiez que JavaScript est activé
- Rechargez la page (F5)
- Vérifiez la console du navigateur (F12)

### Exercices qui ne se Lancent Pas
- Assurez-vous que le serveur Flask fonctionne
- Vérifiez la connexion réseau
- Testez les endpoints API manuellement

### Configuration non Sauvegardée
- Vérifiez que localStorage est activé
- Essayez dans un autre navigateur
- Effacez le cache si nécessaire

### Messages d'Erreur
- Redémarrez le serveur Python
- Vérifiez les logs du serveur
- Contactez le support si le problème persiste

## 📞 Support

### Logs et Diagnostic
```bash
# Vérifier le statut du serveur
curl http://localhost:5000/avatar/motivation

# Tester les exercices
python test_avatar_features.py
```

### Ressources Supplémentaires
- 📖 Documentation complète : `NOUVELLES_FONCTIONNALITES.md`
- 🧪 Tests automatiques : `test_avatar_features.py`
- 🔧 Configuration serveur : `app.py`

---

**🎉 Profitez de votre nouveau compagnon de bien-être personnalisé !**

Votre avatar PsyBot est maintenant prêt à vous accompagner dans votre parcours de bien-être mental. N'hésitez pas à explorer toutes les fonctionnalités et à personnaliser l'expérience selon vos besoins.
