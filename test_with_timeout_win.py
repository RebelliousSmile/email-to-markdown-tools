#!/usr/bin/env python
"""Test with timeout for Windows."""

import sys
import threading
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set a timeout flag
timeout = False

def timeout_handler():
    global timeout
    timeout = True
    print("ERROR: Test timed out!")
    sys.exit(1)

# Start a timer thread
timer = threading.Timer(10.0, timeout_handler)
timer.start()

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
    
    # Cancel the timer if test succeeds
    timer.cancel()
    print("SUCCESS: Test passed!")
    
except Exception as e:
    timer.cancel()
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)