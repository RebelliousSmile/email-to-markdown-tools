---
name: code-review
description: Code review checklist and scoring template
---

# Code Review for folder-classifier feature

Review of: src/folder_classifier.py, scripts/classify.py, scripts/reorganize.py, scripts/summarize.py (classify step addition)

- Status: NEEDS_FIXES
- Confidence: 87%

---

- [Main expected Changes](#main-expected-changes)
- [Scoring](#scoring)
- [Code Quality Checklist](#code-quality-checklist)
- [Final Review](#final-review)

## Main expected Changes

- [x] src/folder_classifier.py — nouveau module ML/LLM de proposition de chemin
- [x] scripts/classify.py — nouveau script CLI de classification interactive
- [x] scripts/reorganize.py — nouveau script CLI de réorganisation de l'arborescence
- [x] scripts/summarize.py — ajout du step classification optionnel + flag --no-classify

## Scoring

- [🔴] **Code dupliqué** `classify.py:60-71` / `reorganize.py:64-73` / `summarize.py:175-207` : la logique `_unique_destination` est réimplémétée 3 fois avec des variations mineures — extraire dans un helper partagé (ex. `src/utils.py`)
- [🔴] **Code dupliqué** `classify.py:25-30` / `reorganize.py:20-25` / `summarize.py:33-38` : `_load_config` est copiée-collée à l'identique dans les 3 scripts — centraliser dans `src/config.py` ou `src/utils.py`
- [🔴] **Code dupliqué** `folder_classifier.py:171-184` / `reorganize.py:75-87` : `_load_corpus` est dupliquée entre le module et le script — le script devrait importer depuis `folder_classifier`
- [🟡] **Sécurité — joblib deserialization** `folder_classifier.py:194-196` : `joblib.load` sur des fichiers `.pkl` arbitraires peut exécuter du code malveillant si le fichier `data/model.pkl` est remplacé — documenter l'hypothèse de confiance ou ajouter un avertissement
- [🟡] **Magic string** `folder_classifier.py:151-155` : les valeurs `"direct"`, `"group"`, `"mailing_list"` et les chemins `"Correspondance/Direct/Divers"` etc. sont des constantes magiques non documentées — les déclarer comme constantes nommées en tête de module
- [🟡] **Magic number** `folder_classifier.py:102` : `response.count("/") != 2` encode implicitement le nombre de niveaux attendus (3) — nommer cette contrainte (`EXPECTED_DEPTH = 3`)
- [🟡] **Gestion d'erreur silencieuse** `folder_classifier.py:145` : `except Exception: pass` avale toutes les erreurs Ollama sans log — au minimum logger l'exception en DEBUG pour faciliter le diagnostic
- [🟡] **Import conditionnel répété** `folder_classifier.py:69,119,161,188,199` : `import ollama`, `import joblib`, `import numpy` sont importés à l'intérieur de fonctions à chaque appel — les placer en tête de fichier avec try/except si optionnels
- [🟡] **Responsabilité mixte** `folder_classifier.py:88-107` : `prompt_user` gère à la fois l'affichage, la validation du format et l'interaction — séparer la validation dans une fonction `_validate_path(response)` pure
- [🟡] **Logique inline dans summarize** `summarize.py:188-210` : le bloc de classification (propose → prompt → move → record) est inliné dans `main()` avec une profondeur d'indentation de 5 niveaux — extraire dans `_classify_output(output_path, category, config)`
- [🟡] **Manque de logging** `reorganize.py` global : aucun logger configuré dans le script, tous les retours utilisateur passent par `print()` sans niveau — cohérent avec `classify.py` mais à unifier
- [🟡] **Chemin corpus sur label absolu** `reorganize.py:98-109` : `_update_corpus` compare des chaînes de chemins absolus (`str(old_abs)`) avec des labels qui sont supposés être relatifs (`Niveau1/Niveau2/Niveau3`) — cette correspondance échouera silencieusement si les labels sont des chemins relatifs
- [🟢] Conventions de nommage respectées (snake_case, fonctions privées préfixées `_`)
- [🟢] Type hints présents sur toutes les signatures publiques
- [🟢] Séparation CLI / logique métier respectée (scripts vs src/)
- [🟢] Gestion de l'encodage UTF-8 Windows correctement traitée dans les 3 scripts
- [🟢] Pas de SQL, pas de frontend — sections non applicables

## Code Quality Checklist

### Potentially Unnecessary Elements

- [🔴] `reorganize.py:12-16` : double import `import io` (lignes 6 et 9) — le bloc UTF-8 est copy-paste depuis classify/summarize, factoriser dans un helper `src/encoding.py` ou au moins dédupliquer localement

### Standards Compliance

- [🟢] Naming conventions followed
- [🟡] Coding rules : imports conditionnels dans les fonctions à corriger

### Architecture

- [🔴] Duplication de `_load_config` et `_load_corpus` entre modules — violation du principe DRY
- [🟡] `reorganize.py` n'importe pas depuis `folder_classifier` alors que les opérations corpus sont déjà encapsulées là

### Code Health

- [🟡] Fonctions `main()` dans classify.py (134 l.) et summarize.py (237 l.) trop longues — à découper
- [🟡] Complexité cyclomatique de `record_decision` acceptable mais limite (3 branches, 2 lectures fichier)
- [🔴] Magic strings/numbers non nommés dans folder_classifier.py
- [🟡] Gestion d'erreur incomplète : `_llm_propose_path` avale les exceptions sans log

### Security

- [🟡] joblib.load sur .pkl non vérifiés (voir scoring)
- [🟢] Pas d'injection SQL
- [🟢] Variables d'environnement lues via `os.environ` (ANTHROPIC_API_KEY) — correct

### Error management

- [🟡] `folder_classifier.py:145` : `except Exception` sans log
- [🟢] Les erreurs parse et groupe sont loggées et comptabilisées dans classify.py et summarize.py

### Performance

- [🟡] `folder_classifier.py:57` : `_load_model` est appelé deux fois dans `record_decision` (ligne 20 dans `propose_path` puis ligne 57) si le corpus était trop petit lors de `propose_path` — cas limite, mais potentiellement redondant
- [🟢] `partial_fit` utilisé correctement pour l'entraînement incrémental

### Backend specific

#### Logging

- [🟡] `reorganize.py` : pas de logger configuré, tout est en `print()`
- [🟢] classify.py et summarize.py ont un logger configuré

## Final Review

- **Score**: 6.5/10
- **Feedback**: Le code est fonctionnel et bien structuré dans l'ensemble. La séparation src/scripts est respectée, les types hints sont présents, et la gestion UTF-8 Windows est correcte. Les problèmes principaux sont la duplication de code (`_load_config`, `_load_corpus`, `_unique_destination`) entre les 3 scripts, les magic strings dans `folder_classifier.py`, et la gestion silencieuse des erreurs Ollama.
- **Follow-up Actions**:
  1. Extraire `_load_config` et `_unique_destination` dans `src/utils.py`
  2. Importer `_load_corpus` depuis `folder_classifier` dans `reorganize.py`
  3. Nommer les constantes de mapping et la profondeur attendue
  4. Ajouter un log DEBUG dans le `except Exception` de `_llm_propose_path`
  5. Extraire le bloc classification de `summarize.py:main()` dans une fonction dédiée
  6. Vérifier la logique de correspondance corpus/labels dans `_update_corpus`
- **Additional Notes**: `reorganize.py:_update_corpus` mérite un test unitaire dédié car la logique de remplacement de chemin sur des labels relatifs vs absolus est fragile.
