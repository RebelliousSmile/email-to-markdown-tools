---
name: coding-assertions
description: Code quality verification checklist
scope: all
---

# Coding Guidelines

> Those rules must be minimal because they MUST be checked after EVERY CODE GENERATION.

## Requirements to complete a feature

- All commands in the "Before commit" and "Before push" tables pass with no errors
- No regressions introduced in existing behavior

## Commands to run

### Before commit

| Order | Command | Description |
| ----- | ------- | ----------- |
| 1 | `python scripts/validate_format.py` | Validate input file format |

### Before push

| Order | Command | Description |
| ----- | ------- | ----------- |
| 1 | `python -m pytest` | Run all tests |
