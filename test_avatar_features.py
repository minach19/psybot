#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour les nouvelles fonctionnalités de l'avatar PsyBot
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"

def test_breathing_exercise():
    """Test de l'endpoint des exercices de respiration"""
    print("🫁 Test des exercices de respiration...")
    try:
        response = requests.get(f"{BASE_URL}/avatar/breathing-exercise")
        if response.status_code == 200:
            data = response.json()
            exercise = data['exercise']
            print(f"   ✅ Exercice reçu: {exercise['name']}")
            print(f"   📝 Description: {exercise['description']}")
            print(f"   ⏱️ Durée: {exercise['duration']} minutes")
            print(f"   📋 Instructions: {len(exercise['instructions'])} étapes")
            return True
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_stretch_exercise():
    """Test de l'endpoint des exercices d'étirement"""
    print("🤸‍♀️ Test des exercices d'étirement...")
    try:
        response = requests.get(f"{BASE_URL}/avatar/stretch-exercise")
        if response.status_code == 200:
            data = response.json()
            exercise = data['exercise']
            print(f"   ✅ Exercice reçu: {exercise['name']}")
            print(f"   📝 Description: {exercise['description']}")
            print(f"   ⏱️ Durée: {exercise['duration']} secondes")
            print(f"   📋 Instructions: {len(exercise['instructions'])} étapes")
            return True
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_motivation():
    """Test de l'endpoint des messages motivationnels"""
    print("💬 Test des messages motivationnels...")
    try:
        response = requests.get(f"{BASE_URL}/avatar/motivation")
        if response.status_code == 200:
            data = response.json()
            message = data['message']
            print(f"   ✅ Message reçu: {message}")
            return True
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_avatar_speak():
    """Test de l'endpoint de parole personnalisée de l'avatar"""
    print("🤖 Test de la parole personnalisée de l'avatar...")
    
    moods = ['positive', 'negative', 'neutral']
    names = ['Marie', 'Jean', 'Alex']
    
    for mood in moods:
        for name in names:
            try:
                payload = {'mood': mood, 'name': name}
                response = requests.post(f"{BASE_URL}/avatar/speak", 
                                       json=payload,
                                       headers={'Content-Type': 'application/json'})
                
                if response.status_code == 200:
                    data = response.json()
                    message = data['message']
                    print(f"   ✅ {mood.capitalize()} pour {name}: {message[:50]}...")
                else:
                    print(f"   ❌ Erreur pour {mood}/{name}: {response.status_code}")
                    return False
                    
                time.sleep(0.1)  # Éviter de surcharger le serveur
                
            except Exception as e:
                print(f"   ❌ Exception pour {mood}/{name}: {e}")
                return False
    
    return True

def test_personality():
    """Test de l'endpoint de personnalité de l'avatar"""
    print("🎭 Test des personnalités d'avatar...")
    
    personalities = ['zen', 'energetic', 'wise']
    
    for personality in personalities:
        try:
            payload = {'personality': personality}
            response = requests.post(f"{BASE_URL}/avatar/personality", 
                                   json=payload,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Personnalité {personality}: {data['emoji']} - {data['message'][:50]}...")
            else:
                print(f"   ❌ Erreur pour {personality}: {response.status_code}")
                return False
                
            time.sleep(0.1)
            
        except Exception as e:
            print(f"   ❌ Exception pour {personality}: {e}")
            return False
    
    return True

def test_all_exercises():
    """Test de l'endpoint de tous les exercices"""
    print("📋 Test de récupération de tous les exercices...")
    try:
        response = requests.get(f"{BASE_URL}/exercises/all")
        if response.status_code == 200:
            data = response.json()
            breathing_count = len(data['breathing_exercises'])
            stretch_count = len(data['stretch_exercises'])
            motivation_count = len(data['motivational_messages'])
            
            print(f"   ✅ Exercices de respiration: {breathing_count}")
            print(f"   ✅ Exercices d'étirement: {stretch_count}")
            print(f"   ✅ Messages motivationnels: {motivation_count}")
            return True
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_server_connectivity():
    """Test de connectivité avec le serveur"""
    print("🌐 Test de connectivité avec le serveur...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("   ✅ Serveur accessible")
            return True
        else:
            print(f"   ❌ Serveur inaccessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Impossible de joindre le serveur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧩 === TEST DES NOUVELLES FONCTIONNALITÉS PSYBOT ===\n")
    
    tests = [
        ("Connectivité serveur", test_server_connectivity),
        ("Exercices de respiration", test_breathing_exercise),
        ("Exercices d'étirement", test_stretch_exercise),
        ("Messages motivationnels", test_motivation),
        ("Parole personnalisée", test_avatar_speak),
        ("Personnalités d'avatar", test_personality),
        ("Tous les exercices", test_all_exercises)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📍 {test_name}")
        print("-" * 50)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name}: RÉUSSI")
        else:
            print(f"❌ {test_name}: ÉCHEC")
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès !")
        print("🚀 L'avatar interactif est pleinement fonctionnel !")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les logs ci-dessus.")
    
    print("\n🔗 Accédez à l'application sur: http://localhost:5000")

if __name__ == "__main__":
    main()
