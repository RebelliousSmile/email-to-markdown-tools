#!/usr/bin/env python3
"""Debug script to test the specific failing test case."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, 'src')

print("Testing the specific failing test case...")

try:
    # Import the function to test
    from src.config import load_config
    print("SUCCESS: Imported load_config")
    
    # Test case: test_load_config_file_not_found
    print("\nRunning test_load_config_file_not_found...")
    
    # Create a mock Path object
    config_path = MagicMock(spec=Path)
    config_path.exists.return_value = False
    config_path.__str__ = lambda self: "/non/existent/path/config.yaml"
    
    print("Created mock config_path with exists=False")
    
    # Mock sys.exit to avoid exiting the test process
    with patch('sys.exit') as mock_exit:
        with patch('sys.stderr.write') as mock_stderr:
            print("Patched sys.exit and sys.stderr.write")
            
            try:
                load_config(config_path)
                print("load_config executed")
                
                # Verify that an error message was printed to stderr
                print("mock_stderr called:", mock_stderr.called)
                if mock_stderr.called:
                    print("stderr calls:", mock_stderr.call_args_list)
                
                # Verify that sys.exit was called with error code 1
                print("mock_exit called:", mock_exit.called)
                if mock_exit.called:
                    print("exit calls:", mock_exit.call_args_list)
                    
            except SystemExit as e:
                print("SystemExit caught:", e)
                print("This is expected behavior for this test")
            
    print("Test completed successfully")
    
except Exception as e:
    print("ERROR:", e)
    import traceback
    traceback.print_exc()

print("\nDebug test completed.")