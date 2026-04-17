---
name: architecture
description: Module architecture and structure
scope: all
---

# Architecture

## Language/Framework

Python CLI tool — no package manifest. Invoked directly via `python scripts/summarize.py`.

```mermaid
---
title: summarize-emails architecture
---
flowchart LR
    CLI["CLI (scripts/summarize.py)"]
    FileIO["File I/O (to-summarize/ → summarized/)"]
    Config["Config (config/config.yaml)"]
    LLM["LLM API"]

    CLI --> FileIO
    CLI --> Config
    CLI --> LLM
```

## Project Structure

```
summarize-emails/
├── scripts/
│   ├── summarize.py          # Main entry point
│   └── validate_format.py    # Input validation
├── to-summarize/             # Input email files
├── summarized/               # Output summaries
└── config/
    └── config.yaml           # Configuration (model, prompts, paths)
```

## Naming Conventions

- **Files**: snake_case
- **Functions**: snake_case
- **Variables**: snake_case
- **Constants**: UPPER_CASE
- **Classes**: PascalCase
