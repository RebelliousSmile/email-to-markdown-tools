#!/usr/bin/env python3
"""Direct test without pytest to isolate the issue."""

import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, 'src')

print("=== Direct Test of Config Module ===")

# Import the function to test
from src.config import load_config
print("OK: Imported load_config successfully")

# Create a mock Path object that doesn't exist
config_path = MagicMock(spec=Path)
config_path.exists.return_value = False
config_path.__str__ = lambda self: "/non/existent/path/config.yaml"
config_path.is_file.return_value = False

print("OK: Created mock config_path")

# Test the function directly
print("Calling load_config with non-existent path...")

# We need to catch the SystemExit that will be raised
try:
    result = load_config(config_path)
    print("ERROR: Unexpected: load_config should have exited but returned:", result)
except SystemExit as e:
    print("OK: SystemExit caught as expected, code:", e.code)
    print("This is the correct behavior - the function exits when file not found")
except Exception as e:
    print("ERROR: Unexpected exception:", e)
    import traceback
    traceback.print_exc()

print("\n=== Test completed ===")