import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    import io
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse
import logging
import shutil

from src.config import load_config
from src.parser import parse_email
from src.folder_classifier import propose_path, record_decision, prompt_user

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def _get_input_dirs(config: dict, account_filter: str | None) -> list[Path]:
    classify_cfg = config.get("classify", {})
    result: list[Path] = []
    for raw_dir in classify_cfg.get("input_dirs", []):
        input_dir = Path(raw_dir)
        if account_filter and account_filter not in input_dir.name:
            continue
        if input_dir.exists():
            result.append(input_dir)
        else:
            logger.warning("Répertoire absent, ignoré: %s", input_dir)
    return result


def _collect_files(config: dict, input_dirs: list[Path]) -> list[Path]:
    classify_cfg = config.get("classify", {})
    exclude_dirs = [d.lower() for d in classify_cfg.get("exclude_dirs", [])]

    files: list[Path] = []
    for input_dir in input_dirs:
        for imap_folder in sorted(input_dir.iterdir()):
            if not imap_folder.is_dir():
                continue
            if imap_folder.name.lower() in exclude_dirs:
                continue
            files.extend(sorted(imap_folder.rglob("*.md")))

    return files


def _imap_hint(filepath: Path, input_dirs: list[Path]) -> list[str]:
    """Return IMAP sub-folder levels that precede the file, minus the INBOX prefix.

    Example: account/INBOX/medias/file.md  →  ["medias"]
             account/INBOX/file.md         →  []
             account/Sent/file.md          →  []
    """
    for input_dir in input_dirs:
        try:
            rel = filepath.parent.relative_to(input_dir)
        except ValueError:
            continue
        parts = list(rel.parts)
        # Strip top-level IMAP folder (e.g. INBOX, Sent) — keep only sub-levels
        if parts:
            top = parts[0]
            sub = parts[1:]
            # Only treat INBOX sub-folders as pre-classification hints
            if top.upper() == "INBOX" and sub:
                return sub
        return []
    return []


def _unique_destination(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify emails interactively into folders.")
    parser.add_argument("--config", default="config/config.yaml", help="Config file path")
    parser.add_argument("--account", default=None, help="Filter input dirs by account name substring")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    classify_cfg = config.get("classify", {})
    output_dir = Path(classify_cfg.get("output_dir", "classified"))

    input_dirs = _get_input_dirs(config, args.account)
    files = _collect_files(config, input_dirs)

    if not files:
        print("Aucun fichier .md trouvé.")
        print("Traité: 0 emails -> 0 classés, 0 ignorés, 0 erreurs")
        sys.exit(0)

    classified = 0
    skipped = 0
    errors = 0

    total = len(files)
    for index, filepath in enumerate(files, start=1):
        try:
            email = parse_email(filepath)
        except Exception as exc:
            logger.warning("Parse échoué %s: %s", filepath.name, exc)
            errors += 1
            continue

        imap_hint = _imap_hint(filepath, input_dirs)
        proposed_path = propose_path(email, config, imap_hint)

        response = prompt_user(email, proposed_path, index, total, output_dir, imap_hint)

        if response == "q":
            print(f"\nTraité: {classified + skipped + errors} emails -> {classified} classés, {skipped} ignorés, {errors} erreurs")
            sys.exit(0)

        if response == "s":
            skipped += 1
            continue

        final_path = proposed_path if response == "" else response
        parts = [p.strip() for p in final_path.split("/")]

        if len(parts) != 3:
            logger.warning("Chemin invalide '%s', doit avoir 3 niveaux. Ignoré.", final_path)
            skipped += 1
            continue

        dest = output_dir / parts[0] / parts[1] / parts[2] / filepath.name
        dest = _unique_destination(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        record_decision(email, final_path, config)
        shutil.move(str(filepath), str(dest))
        classified += 1

    print(f"\nTraité: {len(files)} emails -> {classified} classés, {skipped} ignorés, {errors} erreurs")


if __name__ == "__main__":
    main()
