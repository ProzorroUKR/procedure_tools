"""
The data modules are imported the way Robot imports them, as a top level
``data`` package, so the library directory has to be on the path.
"""

import os
import sys

LIBRARIES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if LIBRARIES_DIR not in sys.path:
    sys.path.insert(0, LIBRARIES_DIR)
