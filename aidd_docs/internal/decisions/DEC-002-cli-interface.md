# Decision: Interface CLI avec flags --input/--output

| Field   | Value                |
| ------- | -------------------- |
| ID      | DEC-002              |
| Date    | 2026-04-17           |
| Feature | summarize.py         |
| Status  | Accepted             |

## Context

Le script `summarize.py` doit être invocable de manière flexible pour permettre de pointer vers différents dossiers d'entrée et de sortie selon le contexte d'exécution.

## Decision

L'interface CLI utilise des flags explicites : `--input /chemin/vers/to-summarize/` et `--output ./summarized/`.

## Alternatives Considered

| Alternative | Pros | Cons | Rejected because |
| ----------- | ---- | ---- | ---------------- |
| Chemins codés en dur | Simple | Pas flexible | Inflexible pour différents environnements |
| Arguments positionnels | Concis | Moins lisible | Moins explicite que des flags nommés |

## Consequences

- `summarize.py` doit utiliser `argparse` ou équivalent
- `validate_format.py` prend le chemin du dossier en argument positionnel
- Interface cohérente et scriptable
