# Decision: Python comme langage principal

| Field   | Value                  |
| ------- | ---------------------- |
| ID      | DEC-001                |
| Date    | 2026-04-17             |
| Feature | Architecture globale   |
| Status  | Accepted               |

## Context

Le projet summarize-emails nécessite un langage pour écrire les scripts de traitement d'emails. L'utilisateur a exprimé une préférence explicite pour Python lors de la phase de conception initiale.

## Decision

Python est utilisé comme seul langage du projet pour tous les scripts (`validate_format.py`, `summarize.py`) et les utilitaires.

## Alternatives Considered

| Alternative | Pros | Cons | Rejected because |
| ----------- | ---- | ---- | ---------------- |
| Node.js     | Bonne intégration LLM SDK | Moins naturel pour scripting fichiers | Préférence utilisateur |
| Bash        | Simple pour I/O fichiers | Difficile à maintenir, pas de LLM SDK | Trop limité pour LLM |

## Consequences

- Tous les scripts doivent être écrits en Python
- Utilisation de `pytest` pour les tests
- Intégration LLM via SDK Python (ex: `anthropic`, `openai`)
