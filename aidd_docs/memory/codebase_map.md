---
name: codebase-structure
description: Project structure documentation
scope: all
---

# Codebase Structure

```mermaid
---
title: email-to-python-tools project structure
---
flowchart TD
  Root["email-to-python-tools/"]
  Config["config/config.yaml"]
  Scripts["scripts/"]
  Src["src/"]
  Data["data/"]
  SummarizeScript["summarize.py"]
  ClassifyScript["classify.py"]
  ReorganizeScript["reorganize.py"]
  ValidateScript["validate_format.py"]
  FolderClassifier["folder_classifier.py"]
  ConfigMod["config.py"]
  CoreModules["parser, categorizer, llm, archiver, ..."]
  Summarizers["summarizers/"]

  Root --> Config
  Root --> Scripts
  Root --> Src
  Root --> Data
  Scripts --> SummarizeScript
  Scripts --> ClassifyScript
  Scripts --> ReorganizeScript
  Scripts --> ValidateScript
  Src --> FolderClassifier
  Src --> ConfigMod
  Src --> CoreModules
  Src --> Summarizers
  Data -->|"corpus.jsonl, known_classes.json, model.pkl"| FolderClassifier
```

## Key Files

| Path | Purpose |
|---|---|
| `config/config.yaml` | Config centrale : LLM, seuils, chemins, section classify |
| `src/folder_classifier.py` | Module partagé : Ollama cold start + BernoulliNB incrémental |
| `src/config.py` | `load_config()` centralisé, importé par tous les scripts |
| `data/corpus.jsonl` | Exemples étiquetés (runtime, gitignored) |
| `data/known_classes.json` | Registre des classes BernoulliNB (runtime, gitignored) |
| `data/model.pkl` | Modèle sérialisé (runtime, gitignored) |
| `data/vectorizer.pkl` | TF-IDF vectorizer sérialisé (runtime, gitignored) |

## Input Sources

Les emails sont produits par `email-to-markdown` (Rust) et organisés par :
```
<emails_root>/<compte_imap>/<dossier_imap>/<email>.md
```

`classify.input_dirs` liste les répertoires de comptes IMAP à traiter (1 niveau de profondeur).
