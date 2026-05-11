# Migration vers Ollama (local) — élimination Anthropic API

**Branch name**: `feat/migrate-ollama`
**Date**: 2026-05-11
**Confidence**: 9/10

## Objectif

Remplacer toutes les dépendances à l'API Anthropic (payante, données envoyées hors réseau) par Ollama local pour garantir la confidentialité des emails traités.

## Flux

```
email .md  →  summarize.py  →  ollama.chat(model, url, prompt)  →  résumé .md
email .md  →  llm.py        →  ollama.chat(model, url, prompt)  →  catégorie
```

## Phases

### Phase 1 — Config

- Remplacer le bloc `llm:` dans `config/config.yaml` par `ollama:` (url + model)
- Plus de clé API

### Phase 2 — Callsites Anthropic (4 fichiers)

- `src/llm.py` : supprimer `_resolve_api_key()`, ajouter `_resolve_url()`, réécrire `classify_email()` avec `ollama.chat()`, corriger `import sys` manquant
- `src/summarizers/filename.py` : changer signature `make_filename(group, category, llm_client)` → `make_filename(group, category, model, url)`, remplacer `llm_client.messages.create()` par `ollama.chat()`
- `scripts/summarize.py` : supprimer `_build_llm_client()`, passer `model` + `url` au lieu de `llm_client`

### Phase 3 — Dépendances + tests

- `requirements.txt` : retirer `anthropic` (ollama déjà présent)
- `tests/test_llm.py` : corriger import `_load_config` → `_get_llm_config`, remplacer mocks Anthropic par `patch('src.llm.ollama.chat')`
