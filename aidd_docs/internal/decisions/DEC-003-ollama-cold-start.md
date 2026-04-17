# Decision: Ollama/Qwen3 comme LLM de cold start

| Field   | Value              |
| ------- | ------------------ |
| ID      | DEC-003            |
| Date    | 2026-04-17         |
| Feature | folder_classifier  |
| Status  | Accepted           |

## Context

Le classifieur de dossiers doit proposer un chemin 3 niveaux sans données d'entraînement au démarrage. Un appel LLM est nécessaire, mais l'API Anthropic est payante et ne doit pas être consommée pour cette tâche secondaire.

## Decision

Utiliser Ollama en local avec le modèle `qwen3:8b` pour les propositions de cold start. Si Ollama n'est pas disponible, fallback sur des heuristiques basées sur `email_type`.

## Alternatives Considered

| Alternative | Pros | Cons | Rejected because |
| ----------- | ---- | ---- | ---------------- |
| Anthropic API | Qualité élevée | Payant, latence réseau | Coût non justifié pour classification de dossiers |
| Règles seules | Gratuit, instantané | Peu précis, non sémantique | Qualité insuffisante pour cold start |
| Groq/Together AI | Gratuit (tier) | Clé API externe, dépendance réseau | Moins autonome qu'Ollama local |

## Consequences

- Ollama doit être installé et `qwen3:8b` téléchargé (`ollama pull qwen3:8b`)
- Fonctionne hors-ligne une fois le modèle téléchargé
- `classify.cold_start_model` dans `config.yaml` permet de changer le modèle
- Fallback automatique sur heuristiques si Ollama indisponible
