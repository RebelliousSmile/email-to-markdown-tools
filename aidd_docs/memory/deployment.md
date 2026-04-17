---
name: deployment
description: Infrastructure and deployment documentation
scope: all
---

# Deployment

## Project Structure

```plaintext
summarize-emails/
├── scripts/
│   ├── validate_format.py
│   └── summarize.py
├── config/
│   ├── config.yaml.example
│   └── config.yaml
├── to-summarize/       # input files
└── summarized/         # output files
```

## Configuration

- `config/config.yaml` — copied from `config/config.yaml.example` before first use
- No environment variables required; all settings live in `config.yaml`
