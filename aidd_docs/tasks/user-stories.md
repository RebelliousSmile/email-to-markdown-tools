# Summarize Emails

## US-01: "Valider les fichiers d'entrée"

**As a** utilisateur d'email2markdown
**I want** valider mes fichiers `.md` avant traitement
**So that** je sache si mon dossier est prêt à être traité

```gherkin
Scenario: Dossier valide
  Given un dossier contenant des fichiers .md bien formés
  When je lance validate_format.py sur ce dossier
  Then j'obtiens un rapport "OK : N fichiers valides"

Scenario: Fichier invalide détecté
  Given un dossier contenant un fichier .md mal formé
  When je lance validate_format.py
  Then j'obtiens la liste des fichiers invalides avec la raison

Scenario: Dossier vide
  Given un dossier sans fichier .md
  When je lance validate_format.py
  Then j'obtiens un avertissement "aucun fichier à traiter"
```

---

## US-02: "Catégoriser et résumer les emails"

**As a** utilisateur d'email2markdown
**I want** traiter un dossier d'emails `.md` et obtenir des résumés adaptés par catégorie et ancienneté
**So that** je passe d'une communication brute à une information triée et exploitable

### Catégories et traitement

| Catégorie | Récent | Ancien |
|---|---|---|
| **Travail** | Fiche complète : chronologie, statut, actions en suspens | Résumé condensé : statut final + date |
| **Notification** | Fiche : action déclenchée + liens | Une ligne : action + date |
| **Newsletter** | Bullet points des éléments notables | Date + titres, pas de lien |
| **Associatif** | Page unique par association, toutes comms agrégées | idem |

```gherkin
Scenario: Emails de travail récents groupés par fil
  Given plusieurs emails .md d'un même échange professionnel de moins de 30 jours
  When je lance summarize.py --input ./to-summarize/ --output ./summarized/
  Then un fichier .md est généré avec chronologie, statut et actions en suspens

Scenario: Emails de travail anciens
  Given un fil professionnel de plus de 30 jours
  When je lance summarize.py
  Then un fichier .md condensé est généré avec statut final et date uniquement

Scenario: Notifications dupliquées
  Given plusieurs emails identiques de notification (ex: 3 emails Firebase identiques)
  When je lance summarize.py
  Then un seul fichier .md est généré avec l'action et la date (doublons supprimés)

Scenario: Newsletter ancienne avec lien "voir en ligne"
  Given une newsletter de plus de 14 jours contenant un URL "voir en ligne"
  When je lance summarize.py
  Then le fichier de sortie contient uniquement ce lien

Scenario: Newsletter ancienne sans lien "voir en ligne"
  Given une newsletter de plus de 14 jours sans URL "voir en ligne"
  When je lance summarize.py
  Then aucun fichier de sortie n'est généré pour cette newsletter

Scenario: Emails associatifs agrégés par source
  Given plusieurs emails d'une même association sur plusieurs mois
  When je lance summarize.py
  Then un seul fichier .md est généré pour cette association avec toutes les comms agrégées chronologiquement

Scenario: Catégorie ambiguë
  Given un email dont la catégorie n'est pas détectable par heuristique
  When je lance summarize.py
  Then le LLM est utilisé en fallback pour déterminer la catégorie

Scenario: Dossier de sortie inexistant
  Given un chemin --output inexistant
  When je lance summarize.py
  Then le dossier est créé automatiquement

Scenario: Nom de fichier de sortie
  Given un groupe d'emails traités
  When le résumé est généré
  Then le fichier est nommé d'après le sujet détecté par le LLM en .md
```

---

## US-03: "Archiver les emails traités"

**As a** utilisateur d'email2markdown
**I want** que les fichiers source soient déplacés après traitement
**So that** mon dossier `to-summarize/` reste propre sans risquer de perdre les originaux

```gherkin
Scenario: Déplacement vers processed/ après traitement réussi
  Given un fichier .md traité avec succès
  When summarize.py termine le traitement
  Then le fichier source est déplacé dans ./processed/

Scenario: Suppression directe avec --delete
  Given l'option --delete passée à summarize.py
  When le traitement est terminé
  Then les fichiers source sont supprimés définitivement (pas de processed/)

Scenario: Échec de traitement — fichier conservé
  Given une erreur lors du traitement d'un fichier
  When summarize.py rencontre l'erreur
  Then le fichier source reste dans to-summarize/ et l'erreur est signalée
```
