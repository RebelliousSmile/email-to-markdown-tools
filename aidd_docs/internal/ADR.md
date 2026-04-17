# Architecture Decision Record (ADR)

This file contains the key architectural decisions made during the project, along with their context and consequences.

## Decision Log

| Date       | ID      | Title                                                                  | Consequences                                      |
| ---------- | ------- | ---------------------------------------------------------------------- | ------------------------------------------------- |
| 2026-04-17 | DEC-001 | [Python comme langage principal](./decisions/DEC-001-python-language.md) | Tous les scripts en Python, pytest, SDK LLM Python |
| 2026-04-17 | DEC-002 | [Interface CLI --input/--output](./decisions/DEC-002-cli-interface.md)   | argparse obligatoire, interface scriptable         |
| 2026-04-17 | DEC-003 | [Ollama/Qwen3 cold start](./decisions/DEC-003-ollama-cold-start.md)      | Ollama requis en local, fallback heuristiques      |
| 2026-04-17 | DEC-004 | [BernoulliNB incrémental](./decisions/DEC-004-bernoullinb-incremental.md) | known_classes.json requis, labels relatifs         |
