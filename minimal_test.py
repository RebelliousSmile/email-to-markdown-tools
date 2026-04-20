#!/usr/bin/env python3
"""Minimal test to identify the blocking point."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path  
sys.path.insert(0, 'src')

print("1. Importing src.config...")
from src.config import load_config
print("   SUCCESS: Imported")

print("2. Creating mock...")
config_path = MagicMock(spec=Path)
config_path.exists.return_value = False
config_path.__str__ = lambda self: "/non/existent/path/config.yaml"
print("   SUCCESS: Mock created")

print("3. Setting up patches...")
with patch('sys.exit') as mock_exit:
    with patch('sys.stderr.write') as mock_stderr:
        print("   SUCCESS: Patches set up")
        
        print("4. Calling load_config...")
        try:
            load_config(config_path)
            print("   load_config completed (unexpected)")
        except SystemExit:
            print("   SystemExit caught (expected)")
        except Exception as e:
            print("   Exception caught:", e)
            
        print("5. Checking mock calls...")
        print("   stderr.write called:", mock_stderr.called)
        print("   sys.exit called:", mock_exit.called)

print("Test completed.")