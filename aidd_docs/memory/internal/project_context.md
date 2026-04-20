# Project Context

## Overview
- **Project Name**: email-to-python-tools
- **Domain**: Email processing and classification using AI/LLM.
- **Type**: Python CLI tools for local email file processing.

## Technologies
- **Language**: Python 3.13
- **AI/LLM**: Anthropic API (for summarization), Ollama (for cold-start classification)
- **Machine Learning**: Scikit-learn (BernoulliNB for incremental classification)
- **Testing**: Pytest (unit tests), Coverage.py (coverage reporting)
- **Configuration**: YAML-based configuration files

## Key Features
- **Email Summarization**: Generate concise summaries of emails using LLM.
- **Email Classification**: Interactive classification of emails into folders with incremental ML.
- **Validation**: Ensure email files conform to the expected format before processing.
- **Reorganization**: Restructure the folder tree interactively.

## Architecture
- **Modular Design**: Separation of concerns with reusable modules in `src/`.
- **CLI Scripts**: Scripts in `scripts/` for specific tasks (summarize, classify, etc.).
- **Configuration-Driven**: Centralized configuration via `config/config.yaml`.
- **Incremental Learning**: ML models are trained incrementally based on user feedback.

## Workflow
1. **Input**: Email files are exported by `email-to-markdown` and placed in input directories.
2. **Validation**: `validate_format.py` checks the format of email files.
3. **Processing**: `summarize.py` or `classify.py` processes the emails.
4. **Output**: Summaries and classified emails are written to output directories.
5. **Learning**: ML models are updated based on user decisions during classification.

## Dependencies
- **Python Libraries**: `anthropic`, `ollama`, `scikit-learn`, `pytest`, `coverage`, etc.
- **External Tools**: Ollama (for local LLM), Git (for version control).

## Future Directions
- **Improved ML Models**: Explore more advanced models for classification.
- **Enhanced UI**: Add a graphical interface for interactive classification.
- **Performance Optimization**: Optimize processing speed for large email datasets.
