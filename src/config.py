import sys
from pathlib import Path

import yaml


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        print(f"Erreur: fichier de configuration introuvable: {config_path}", file=sys.stderr)
        sys.exit(1)
    with config_path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
