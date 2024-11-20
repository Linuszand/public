# custom.py

import pytest
import sys
import os

def run_tests():
    # Ensure that the 'src' folder is in the PYTHONPATH
    sys.path.insert(0, os.path.abspath('src'))

    # Run pytest with options

    result = pytest.main([
        'src',            # The directory where the tests are located
        '--maxfail=1',    # Stop after the first failure (optional)
        '--disable-warnings', # Disable warnings in the output
        '-q',             # Quiet mode, for cleaner output
        '--tb=short',      # Short traceback (optional)
        '-v',
        '-p', 'no:warning',
        '-W', 'always'
    ])

    # Return the result code so that it can be handled by the shell script
    sys.exit(result)

if __name__ == "__main__":
    run_tests()

