""" Module for testing the clean.py functions. """

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
from datetime import datetime, timedelta

# project root as a Path
proj_root = Path(__file__).resolve().parent.parent
# add project root to sys.path for imports
sys.path.insert(0, str(proj_root))
