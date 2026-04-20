from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_EMAIL_TYPE_PATHS = {
    "direct": "Correspondance/Direct/Divers",
    "group": "Correspondance/Groupes/Divers",
    "mailing_list": "Listes/Divers/Divers",
}
_DEFAULT_PATH = "Divers/Divers/Divers"


def propose_path(email: dict, config: dict) -> str:
    classify_cfg = config.get("classify", {})
    data_dir = Path(classify_cfg.get("data_dir", "data"))
    threshold: float = classify_cfg.get("confidence_threshold", 0.75)
    min_samples: int = classify_cfg.get("min_samples_before_ml", 20)
    cold_start_model: str = classify_cfg.get("cold_start_model", "qwen3:8b")

    corpus = _load_corpus(data_dir)

    if len(corpus) < min_samples:
        return _llm_propose_path(email, cold_start_model)

    model, vectorizer = _load_model(data_dir)
    if model is None or vectorizer is None:
        return _llm_propose_path(email, cold_start_model)

    label, confidence = _ml_propose_path(email, model, vectorizer)
    if confidence < threshold:
        return _llm_propose_path(email, cold_start_model)
    return label


def record_decision(email: dict, path: str, config: dict) -> None:
    classify_cfg = config.get("classify", {})
    data_dir = Path(classify_cfg.get("data_dir", "data"))
    data_dir.mkdir(parents=True, exist_ok=True)

    corpus_path = data_dir / "corpus.jsonl"
    entry = {
        "subject": email.get("subject", ""),
        "sender": email.get("sender", ""),
        "email_type": email.get("email_type"),
        "label": path,
    }
    with corpus_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    known_classes_path = data_dir / "known_classes.json"
    if known_classes_path.exists():
        with known_classes_path.open(encoding="utf-8") as fh:
            all_known_classes: list[str] = json.load(fh)
    else:
        all_known_classes = []

    if path not in all_known_classes:
        all_known_classes.append(path)
        with known_classes_path.open("w", encoding="utf-8") as fh:
            json.dump(all_known_classes, fh, ensure_ascii=False)

    model, vectorizer = _load_model(data_dir)
    if model is None or vectorizer is None:
        logger.info("Modèle non trouvé, reconstruction depuis le corpus...")
        rebuild_model_from_corpus(data_dir)
        return

    features = _extract_features(entry)
    X = vectorizer.transform([features])
    
    # Ensure classes are consistent with existing model classes
    existing_classes = list(model.classes_)
    if set(all_known_classes) != set(existing_classes):
        # Rebuild model if new classes are added
        logger.info("Nouvelle classe détectée, reconstruction du modèle...")
        rebuild_model_from_corpus(data_dir)
        model, vectorizer = _load_model(data_dir)
        if model is None or vectorizer is None:
            return
        # Retransform features with the new vectorizer
        X = vectorizer.transform([features])
    
    # Use the existing model classes to avoid mismatch
    model.partial_fit(X, [path], classes=None)
    _save_model(model, vectorizer, data_dir)
    logger.info("Modèle mis à jour avec la décision utilisateur : %s", path)


def rebuild_model_from_corpus(data_dir: Path) -> None:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import BernoulliNB

    corpus = _load_corpus(data_dir)
    if not corpus:
        logger.warning("Corpus vide, impossible de reconstruire le modèle.")
        return

    logger.info("Reconstruction du modèle depuis %d exemples...", len(corpus))
    # Filter out corrupted entries
    valid_entries = [e for e in corpus if "label" in e and "subject" in e and "sender" in e]
    if not valid_entries:
        logger.warning("Aucune entrée valide dans le corpus, impossible de reconstruire le modèle.")
        return
    
    texts = [_extract_features(e) for e in valid_entries]
    labels = [e["label"] for e in valid_entries]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = BernoulliNB()
    model.fit(X, labels)

    _save_model(model, vectorizer, data_dir)
    logger.info("Modèle reconstruit et sauvegardé avec succès.")


def prompt_user(email: dict, proposed_path: str) -> str:
    date_val = email.get("date", "")
    print(f"Sujet    : {email.get('subject', '')}")
    print(f"Expéditeur: {email.get('sender', '')}")
    print(f"Date     : {date_val}")
    print(f"Chemin proposé: {proposed_path}")
    response = input(
        "[Entrée] pour accepter, 's' pour ignorer, 'q' pour quitter, "
        "ou saisir un chemin alternatif : "
    ).strip()

    if response in ("", "s", "q"):
        return response

    if response.count("/") != 2:
        print(
            f"Avertissement : le chemin '{response}' n'est pas au format "
            "Niveau1/Niveau2/Niveau3 (2 séparateurs '/' attendus)."
        )
    return response


def _extract_features(email: dict) -> str:
    subject = email.get("subject") or ""
    sender = email.get("sender") or ""
    email_type = email.get("email_type") or ""
    return f"{subject} {sender} {email_type}"


def _llm_propose_path(email: dict, cold_start_model: str) -> str:
    try:
        import ollama

        subject = email.get("subject", "")
        sender = email.get("sender", "")
        email_type = email.get("email_type", "")

        prompt = (
            "Tu es un assistant de classement d'emails. "
            "Réponds UNIQUEMENT par un chemin de dossier au format exact "
            "'Niveau1/Niveau2/Niveau3'. "
            "Exemples valides : 'Travail/Projets/ClientX', 'Personnel/Famille/Vacances'. "
            "Ne retourne RIEN d'autre (pas d'explications, pas de ponctuation, pas de guillemets).\n\n"
            f"Sujet : {subject}\n"
            f"Expéditeur : {sender}\n"
            f"Type d'email : {email_type}\n\n"
            "Propose un chemin de classement à 3 niveaux :"
        )

        response = ollama.chat(
            model=cold_start_model,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response["message"]["content"].strip()
        # Keep only the first line in case model adds extra text
        first_line = raw.splitlines()[0].strip() if raw else ""
        
        # Validation stricte du format
        if first_line.count("/") == 2:
            # Vérifier les caractères interdits
            invalid_chars = ['?', '*', '"', '<', '>', '|']
            if any(char in first_line for char in invalid_chars):
                logger.warning("Chemin LLM invalide (caractères interdits) : %s", first_line)
                return _rule_based_propose(email)
            # Limiter la longueur des niveaux
            parts = first_line.split("/")
            if all(len(part.strip()) <= 50 for part in parts):
                return first_line
        logger.warning("Chemin LLM invalide (format) : %s", first_line)
        return _rule_based_propose(email)
    except Exception as exc:
        logger.debug("LLM propose échoué: %s", exc)
        return _rule_based_propose(email)


def _rule_based_propose(email: dict) -> str:
    email_type = email.get("email_type")
    return _EMAIL_TYPE_PATHS.get(email_type, _DEFAULT_PATH)


def _ml_propose_path(email: dict, model: Any, vectorizer: Any) -> tuple[str, float]:
    import numpy as np

    features = _extract_features(email)
    X = vectorizer.transform([features])
    proba = model.predict_proba(X)[0]
    max_idx = int(np.argmax(proba))
    label = model.classes_[max_idx]
    confidence = float(proba[max_idx])
    return label, confidence


def _load_corpus(data_dir: Path) -> list[dict]:
    corpus_path = data_dir / "corpus.jsonl"
    if not corpus_path.exists():
        return []
    entries = []
    with corpus_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def _load_model(data_dir: Path) -> tuple[Any, Any]:
    import joblib

    model_path = data_dir / "model.pkl"
    vectorizer_path = data_dir / "vectorizer.pkl"
    if not model_path.exists() or not vectorizer_path.exists():
        return None, None
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer


def _save_model(model: Any, vectorizer: Any, data_dir: Path) -> None:
    import joblib

    model_path = data_dir / "model.pkl"
    vectorizer_path = data_dir / "vectorizer.pkl"
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
