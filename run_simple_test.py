#!/usr/bin/env python
"""Simple test runner that bypasses pytest issues."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the test
from tests.test_config import test_load_config_file_not_found

print("Running test_load_config_file_not_found...")
try:
    test_load_config_file_not_found()
    print("✓ Test passed!")
except Exception as e:
    print(f"✗ Test failed: {e}")
    sys.exit(1)