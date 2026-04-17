"""Anthropic LLM wrapper — minimal interface for category fallback."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def _load_config() -> dict[str, Any]:
    """Load config.yaml from the project root config directory, if present."""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    if config_path.exists():
        with config_path.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return {}


def classify_email(subject: str, body_excerpt: str) -> str:
    """Ask the LLM to classify an email into one of the four categories.

    Returns one of: travail, notification, newsletter, associatif.
    Defaults to 'travail' when the response is unparseable or the API fails.
    """
    config = _load_config()
    api_key: str = (
        config.get("llm", {}).get("api_key", "")
        or os.environ.get("ANTHROPIC_API_KEY", "")
    )
    model: str = config.get("llm", {}).get("model", "claude-haiku-4-5")

    prompt = (
        "Classify the following email into exactly one of these categories:\n"
        "travail, notification, newsletter, associatif\n\n"
        f"Subject: {subject}\n"
        f"Body (excerpt): {body_excerpt}\n\n"
        "Reply with only the category name, nothing else."
    )

    try:
        import anthropic  # local import — optional dependency

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=16,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip().lower()
    except Exception:
        return "travail"

    valid = {"travail", "notification", "newsletter", "associatif"}
    return raw if raw in valid else "travail"
