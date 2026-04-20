#!/usr/bin/env python
"""Minimal test to check basic functionality."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing basic import...")
try:
    from src.config import load_config
    print("SUCCESS: src.config imported")
    print("Function load_config:", load_config)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)