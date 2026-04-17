# Decision: BernoulliNB incrémental avec registre de classes dynamique

| Field   | Value              |
| ------- | ------------------ |
| ID      | DEC-004            |
| Date    | 2026-04-17         |
| Feature | folder_classifier  |
| Status  | Accepted           |

## Context

Le classifieur de dossiers doit s'améliorer au fil des validations utilisateur sans ré-entraînement complet. Les dossiers de destination étant créés dynamiquement, le modèle doit accepter de nouvelles classes à tout moment.

## Decision

BernoulliNB avec `partial_fit()` pour l'apprentissage incrémental. Un fichier `data/known_classes.json` maintient le registre de toutes les classes vues, passé à chaque appel `partial_fit(classes=all_known_classes)` pour éviter les crashes sur nouvelles classes.

## Alternatives Considered

| Alternative | Pros | Cons | Rejected because |
| ----------- | ---- | ---- | ---------------- |
| Logistic Regression | Précision similaire | `partial_fit` moins stable | BernoulliNB plus simple pour texte binaire |
| Réentraînement complet | Stable | Lent, bloque l'UX interactive | Non adapté à une session interactive |
| Embeddings + cosinus | Pas de données requises | Dépendance modèle embedding | Complexité inutile pour MVP |

## Consequences

- `data/known_classes.json` doit toujours être synchronisé avec le corpus
- `rebuild_model_from_corpus()` permet de reconstruire si le pkl est corrompu
- Labels corpus en chemins relatifs (`Niveau1/Niveau2/Niveau3`) — jamais absolus
- Le modèle prend le relais après `min_samples_before_ml` exemples (défaut: 20)
- Fallback LLM si confidence < `confidence_threshold` (défaut: 0.75)
