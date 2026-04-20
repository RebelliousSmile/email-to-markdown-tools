#!/usr/bin/env python
"""Test with timeout to prevent hanging."""

import sys
import signal
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def timeout_handler(signum, frame):
    print("ERROR: Test timed out!")
    sys.exit(1)

# Set a 10-second timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)

try:
    print("Running test with timeout...")
    
    from unittest.mock import patch, MagicMock
    from src.config import load_config
    
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
    
    print("SUCCESS: Test passed!")
    signal.alarm(0)  # Cancel the timeout
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)