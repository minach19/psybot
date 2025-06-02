# Guide d'Implémentation des Animations Avatar PsyBot

## Vue d'Ensemble

Ce document explique comment créer et implémenter les animations pour le système d'avatar personnalisable de PsyBot. Les animations Lottie sont utilisées pour donner vie à l'avatar pendant les différents exercices de bien-être.

## 1. Prérequis

### Logiciels Recommandés
- **Adobe After Effects** - Pour la création des animations
- **Bodymovin Plugin** - Pour exporter les animations au format Lottie JSON
- **Adobe Illustrator** - Pour créer les assets vectoriels
- **LottieFiles Preview** - Pour tester les animations

### Alternatives Gratuites/Open Source
- **Synfig Studio** - Alternative gratuite à After Effects
- **Inkscape** - Alternative gratuite à Illustrator
- **LottieFiles Web Editor** - Pour modifications simples d'animations existantes

## 2. Structure des Fichiers Animation

```
static/
└── animations/
    ├── default_animation.json
    ├── breathing/
    │   ├── calming.json
    │   ├── energizing.json
    │   ├── focus.json
    │   └── grounding.json
    ├── stretching/
    │   ├── neck.json
    │   ├── shoulder.json
    │   ├── wrist.json
    │   └── back.json
    ├── mood/
    │   ├── celebration.json
    │   ├── empathy.json
    │   ├── calming.json
    │   ├── supportive.json
    │   ├── neutral.json
    │   └── attentive.json
    └── interaction/
        ├── greeting.json
        ├── listening.json
        └── congratulating.json
```

## 3. Création des Animations Lottie

### Paramètres Recommandés
- **Taille du Canevas**: 512x512 pixels
- **Fréquence d'Images**: 30 fps
- **Durée**:
  - Animations de respiration: 4-8 secondes en boucle
  - Animations d'étirement: 3-5 secondes en boucle
  - Animations d'interaction: 2-3 secondes
- **Format d'Export**: JSON Lottie (via Bodymovin)

### Optimisation
- Minimiser la complexité des formes
- Éviter les effets complexes non pris en charge par Lottie
- Optimiser la taille du fichier JSON (idéalement <100KB)

## 4. Ressources pour les Animations

### Sites d'Animations Prêtes à l'Emploi
- **LottieFiles**: https://lottiefiles.com/ (Certaines animations gratuites, d'autres payantes)
- **IconScout**: https://iconscout.com/ (Abonnement requis pour la plupart des assets)
- **Mixkit**: https://mixkit.co/ (Animations gratuites, mais sélection limitée)

### Services de Création d'Animations sur Mesure
- **Fiverr**: Nombreux animateurs proposant des services Lottie (50-200€ par animation)
- **Upwork**: Freelancers spécialisés en animation (tarifs variables)
- **99designs**: Pour un concours de design d'animations (budget plus élevé)

## 5. Implémentation des Animations

### Intégration dans le Code
Les animations sont chargées via la fonction `loadLottieAnimation` dans `main.js`:

```javascript
function loadLottieAnimation(animationUrl) {
    const container = document.getElementById('lottieAvatar');
    if (!container) return;

    if (lottieAnimation) {
        lottieAnimation.destroy();
    }
    
    lottieAnimation = lottie.loadAnimation({
        container: container,
        renderer: 'svg',
        loop: true,
        autoplay: false,
        path: animationUrl
    });
}
```

### Mapping des Animations selon la Configuration Avatar

Le mapping est défini dans `main.js` via l'objet `lottieAnimationUrls`. Pour l'exemple des exercices de respiration:

```javascript
const lottieAnimationUrls = {
    breathing: {
        light: { 
            sport: '/static/animations/breathing/calming_light_sport.json', 
            casual: '/static/animations/breathing/calming_light_casual.json',
            // ...autres styles
        },
        medium: {
            // configurations pour teint moyen
        },
        dark: {
            // configurations pour teint foncé
        }
    },
    // autres types d'exercices
};
```

## 6. Animations Prioritaires à Créer

1. **Animation de Respiration Calmante** - Pour les exercices de respiration
   - Mouvement pulsatile doux, mimant une respiration profonde
   - Colors apaisantes (bleus, violets clairs)

2. **Animation d'Étirement de Base** - Pour les exercices corporels
   - Mouvement d'extension/flexion des membres
   - Transition fluide entre les positions

3. **Animation Empathique** - Pour répondre à un état émotionnel détecté
   - Expression faciale douce et attentive
   - Léger mouvement d'inclinaison de la tête

## 7. Test et Validation

1. **Compatibilité Navigateur** - Tester sur Chrome, Firefox, Safari
2. **Performance** - Vérifier la fluidité sur appareils moins puissants
3. **Intégration** - Confirmer que les animations se chargent correctement avec différentes configurations d'avatar

## 8. Achats Recommandés

Si la création d'animations personnalisées n'est pas possible, voici quelques recommandations d'achat:

1. **LottieFiles Pro** (19€/mois) - Accès à des milliers d'animations premium
2. **Animation Pack "Wellness & Meditation"** sur CodeCanyon (~49€) - Pack complet d'animations de bien-être
3. **Animateur Freelance** sur Fiverr/Upwork (~150-300€) - Pour un ensemble personnalisé de 5-10 animations

## 9. Ressources Additionnelles

- **Documentation Lottie**: https://airbnb.io/lottie/#/
- **Tutoriel After Effects pour Lottie**: https://www.youtube.com/watch?v=5XMUw_43eTM
- **Guide d'Optimisation Lottie**: https://lottiefiles.com/blog/working-with-lottie/lottie-animation-optimization-guide

## 10. Intégration avec la Détection d'Humeur

L'intégration entre les animations et le système de détection d'humeur se fait via la classe `AvatarMoodIntegration` dans le fichier `avatar-mood-integration.js`.

Lorsqu'une humeur est détectée avec un niveau de confiance suffisant, l'animation correspondante sera jouée et une suggestion d'exercice adaptée sera proposée à l'utilisateur.

---

Document préparé pour l'équipe de développement de PsyBot.
