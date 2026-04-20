#!/usr/bin/env python
"""Simple test approach without complex mocking."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing load_config with non-existent file...")

from src.config import load_config
from unittest.mock import MagicMock

# Create a mock Path object that doesn't exist
config_path = MagicMock(spec=Path)
config_path.exists.return_value = False
config_path.__str__ = lambda self: "/non/existent/path/config.yaml"

try:
    # This should raise SystemExit
    load_config(config_path)
    print("ERROR: Expected SystemExit but function returned normally")
    sys.exit(1)
except SystemExit as e:
    # This is what we expect
    print(f"SUCCESS: Got expected SystemExit with code: {e.code}")
except Exception as e:
    print(f"ERROR: Got unexpected exception: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)