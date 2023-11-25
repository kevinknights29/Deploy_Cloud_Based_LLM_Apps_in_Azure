from __future__ import annotations

import os


# Directories
UTILS_FOLDER = os.path.dirname(os.path.abspath(__file__))
PROJECT_PACKAGE = os.path.dirname(UTILS_FOLDER)
ROOT = os.path.dirname(PROJECT_PACKAGE)

# Files
CONFIG_FILE = os.path.join(ROOT, "config.yaml")

# Logging
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
