#!/usr/bin/env python3
"""Debug script to test imports and configuration."""

import sys
import os
from pathlib import Path

print("Python executable:", sys.executable)
print("Python path:", sys.path)

# Test importing the config module
try:
    print("\nTrying to import src.config...")
    import src.config
    print("SUCCESS: src.config imported successfully")
    
    # Test creating a Path object
    print("\nTesting Path creation...")
    config_path = Path("config/config.yaml")
    print("SUCCESS: Path object created:", config_path)
    print("  Exists:", config_path.exists())
    
    # Test load_config function
    print("\nTesting load_config function...")
    result = src.config.load_config(config_path)
    print("SUCCESS: load_config executed successfully")
    print("  Result type:", type(result))
    print("  Result keys:", list(result.keys()) if isinstance(result, dict) else "Not a dict")
    
except Exception as e:
    print("ERROR:", e)
    import traceback
    traceback.print_exc()

print("\nDebug script completed.")