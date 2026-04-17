# Master Plan: Email Folder Classifier with Incremental Learning

## Overview

- **Goal**: Add an interactive folder classification system to classify kept emails into a user-defined 3-level tree, shared between classify.py and summarize.py, with an incremental ML model that improves over time
- **Risk Score**: 7/10
- **Branch**: `feat/email-classifier/`

## Child Plans

| #   | Plan                          | File                                    | Status  | Validated |
| --- | ----------------------------- | --------------------------------------- | ------- | --------- |
| 1   | Setup + Shared Classifier     | `./2026_04_17-email-classifier-part-1.md` | pending | [ ]       |
| 2   | classify.py                   | `./2026_04_17-email-classifier-part-2.md` | blocked | [ ]       |
| 3   | Extend summarize.py           | `./2026_04_17-email-classifier-part-3.md` | blocked | [ ]       |
| 4   | reorganize.py                 | `./2026_04_17-email-classifier-part-4.md` | blocked | [ ]       |

## Validation Protocol

1. Complete Part 1, verify config + ML module unit tests pass
2. [ ] Checkpoint 1: User confirms ML module works standalone
3. Complete Part 2, run classify.py on real IMAP folder
4. [ ] Checkpoint 2: User confirms classification + file moves work
5. Complete Part 3, run full summarize.py pipeline with classification step
6. [ ] Checkpoint 3: User confirms corpus is shared correctly
7. Complete Part 4, test reorganize.py on existing tree
8. [ ] Final: Integration test across all scripts

## Estimations

- **Confidence**: 8/10
- **Duration**: 3-4 sessions
