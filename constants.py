# This file contains a few reusable values.
# Note that database credentials must be managed separately for security purposes.

import os

import encoders

# Data (text) file locations
DATA_DIR = "data"
DATA_INTAKE_DIR = os.path.join(DATA_DIR, "intake")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_SIMPLIFIED_DIR = os.path.join(DATA_DIR, "simplified")
DATA_ENCODED_DIR = os.path.join(DATA_DIR, "encoded")

OUTPUT_MIN = 0
OUTPUT_MAX = len(encoders.CHARSET)-1
CUSTOM_LOSS_MODULO = OUTPUT_MAX+1

USE_CUSTOM_METRICS = True