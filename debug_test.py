#!/usr/bin/env python
"""Debug script to run the test step by step."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Step 1: Importing test dependencies...")
try:
    import pytest
    from unittest.mock import patch, MagicMock
    import yaml
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

print("\nStep 2: Importing src.config...")
try:
    from src.config import load_config
    print("✓ src.config imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

print("\nStep 3: Running test_load_config_file_not_found...")
try:
    # Create a mock Path object
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = False
    config_path.__str__ = lambda self: "/non/existent/path/config.yaml"
    
    # Mock sys.exit to avoid exiting the test process
    with patch('sys.exit') as mock_exit:
        with patch('sys.stderr.write') as mock_stderr:
            load_config(config_path)
            
            # Verify that an error message was printed to stderr
            mock_stderr.assert_called_once()
            assert "Erreur: fichier de configuration introuvable" in mock_stderr.call_args[0][0]
            
            # Verify that sys.exit was called with error code 1
            mock_exit.assert_called_once_with(1)
    
    print("✓ Test passed!")
except Exception as e:
    print(f"✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)