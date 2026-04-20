# Master Plan : Correction du Delta du Projet

## Contexte
Corriger les écarts identifiés entre les fonctionnalités planifiées et l'implémentation actuelle du projet `email-to-python-tools`.

## Phase 0 : Prérequis et Configuration
**Objectif** : Préparer l'environnement et les dépendances nécessaires.

**Tâches** :
- [ ] Vérifier l'installation d'Ollama (`ollama pull qwen3:8b`).
- [ ] Configurer les clés API pour Anthropic si nécessaire.
- [ ] Créer le dossier `tests/` et configurer `pytest.ini`.
- [ ] Vérifier la disponibilité des données d'entraînement dans `data/`.

**Risques** :
- Ollama doit être installé et accessible localement.
- Les clés API doivent être valides pour les appels LLM.

## Objectifs
1. Intégrer Ollama comme fallback pour la classification.
2. Améliorer l'apprentissage incrémental du modèle ML.
3. Ajouter des tests unitaires pour une couverture minimale.
4. Documenter les modèles ML et leurs processus.

## Phases d'implémentation

### Phase 1 : Intégration d'Ollama pour le Cold Start
**Objectif** : Ajouter un fallback vers Ollama lorsque la confiance du modèle BernoulliNB est faible.

**Tâches** :
- [ ] Analyser le code actuel de `classify.py` pour identifier où intégrer Ollama.
- [ ] Implémenter un mécanisme de fallback si `confiance < 0.75`.
- [ ] Tester le fallback avec des exemples concrets.
- [ ] Documenter la logique de fallback dans le `README.md`.
- [ ] Ajouter un diagramme Mermaid pour expliquer le workflow de fallback.

**Risques** :
- Ollama doit être installé et configuré localement.
- Latence potentielle lors de l'appel à Ollama.

### Phase 2 : Amélioration de l'Apprentissage Incrémental
**Objectif** : S'assurer que le modèle ML est mis à jour correctement après chaque décision utilisateur.

**Tâches** :
- [ ] Vérifier la fonction `rebuild_model_from_corpus` dans `folder_classifier.py`.
- [ ] Ajouter des logs pour suivre les mises à jour du modèle.
- [ ] Tester l'apprentissage incrémental avec un jeu de données simulé.
- [ ] Documenter le processus dans `aidd_docs/memory/internal/ml_model_process.md`.
- [ ] Implémenter un mécanisme de sauvegarde automatique du modèle après chaque mise à jour.
- [ ] Ajouter une validation croisée pour éviter le surapprentissage.

**Risques** :
- Le corpus doit être suffisamment grand pour éviter le surapprentissage.
- Les décisions utilisateur doivent être enregistrées correctement.

### Phase 3 : Ajout de Tests Unitaires
**Objectif** : Créer des tests pour les modules critiques et configurer `pytest`.

**Tâches** :
- [ ] Créer un dossier `tests/` si absent.
- [ ] Ajouter des tests pour `parser.py`, `folder_classifier.py`, et `classify.py`.
- [ ] Configurer `pytest` et `coverage` pour mesurer la couverture.
- [ ] Exécuter les tests et corriger les échecs.
- [ ] Lister les fonctions critiques à tester (ex: `propose_path`, `record_decision`).
- [ ] Ajouter des exemples de tests pour les edge cases (fichiers corrompus, métadonnées manquantes).

**Risques** :
- Les tests doivent couvrir les cas d'erreur et les edge cases.
- La configuration de `pytest` doit être compatible avec le projet.

### Phase 4 : Documentation des Modèles ML
**Objectif** : Documenter le processus de reconstruction du modèle et ajouter des exemples.

**Tâches** :
- [ ] Documenter `rebuild_model_from_corpus` dans `aidd_docs/memory/internal/ml_model_process.md`.
- [ ] Ajouter des exemples d'utilisation dans le `README.md`.
- [ ] Clarifier le seuil de confiance et le fallback vers Ollama.
- [ ] Ajouter un diagramme Mermaid dans le `README.md` pour expliquer le workflow de fallback.

**Risques** :
- La documentation doit être claire pour les nouveaux contributeurs.

## Confidence Assessment
- **✅ Points forts** :
  - Les scripts principaux sont déjà implémentés.
  - La structure modulaire facilite les modifications.
  - Ollama est déjà mentionné dans le `README.md`.
  - Phase 0 ajoutée pour couvrir les prérequis.

- **❌ Risques résiduels** :
  - Intégration d'Ollama non testée dans le code actuel.
  - Apprentissage incrémental partiellement documenté.
  - Tests unitaires absents pour certains modules.

**Score de confiance** : 9/10 (risques résiduels mineurs, plan complet et détaillé).

## Prochaine Étape
Valider ce plan avec l'utilisateur avant de commencer l'implémentation.