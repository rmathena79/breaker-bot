# This file organizes pre-trained models, and facilitates loading them.
# Note scaler value files are tracked a little differently since the same
# scaler can be used for multiple models. Scaler files have the necessary
# information embedded in their names.

import tensorflow as tf
import os

from constants import *
from tf_helpers import *

# Model for inferring the key from Caesar-encrypted text:
CAESAR_KEY_MODEL = os.path.join(MODEL_DIR, "caesar_key_0256_0003.keras")

# Model for inferring plaintext from Caesar-encrypted text:
CAESAR_TEXT_MODEL = os.path.join(MODEL_DIR, "caesar_text_0256_0001.keras")

# Load model from file, including custom objects used throughout this project
def load_model(path: str) -> tf.keras.Model:
    return tf.keras.models.load_model(path,
                custom_objects={
                    'modulo_distance_loss': modulo_distance_loss,
                    'modulo_distance_accuracy': modulo_distance_accuracy,
                    'modulo_rounded_accuracy': modulo_rounded_accuracy,
                    'modulo_output': modulo_output
            })