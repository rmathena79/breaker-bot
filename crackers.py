import numpy as np

import encoders
import helpers
import tf_helpers

# This class wraps up use of a model to try to predict keys or plaintext.
# I wrote it with the Caesar Cipher in mind, but I'm not sure the code is really much
# different for the other ciphers. It may just be that key size is different.
#
# The dimension for the "best guess" seems to be different between the two,
# which is strange.
class Caesar_Cracker(object):
    def __init__(self, scaler, key_model, text_model):
        self.scaler = scaler
        self.key_model = key_model
        self.text_model = text_model

    def infer_text_with_model(self, ciphertext: str) -> str:
        chunk_size = self.text_model.input_shape[2]
        offsets = encoders.string_to_offsets(ciphertext)
        chunks = helpers.chunkify(offsets, chunk_size)
        scaled_chunks = self.scaler.transform(chunks)
        shaped_chunks = tf_helpers.reshape_input(np.array(scaled_chunks), chunk_size)
        guesses = self.text_model.predict(shaped_chunks, verbose=0)
        # Shape of prediction:
        # (chunk count, chunk size, chunk size)
        # ... so that's a little confusing. The best text guesses seem to be along
        # the 3rd dimension, and I don't know why:
        best_guesses = guesses[:, :, chunk_size-1]

        # Now we have floating point offsets. We want integer offsets, then strings:
        flat = best_guesses.flatten()        
        int_offsets = flat.round().astype(int)
        result = encoders.offsets_to_string(int_offsets)

        return result

    def infer_key_with_model(self, ciphertext: str) -> int:
        chunk_size = self.key_model.input_shape[2]
        offsets = encoders.string_to_offsets(ciphertext)
        chunks = helpers.chunkify(offsets, chunk_size)
        scaled_chunks = self.scaler.transform(chunks)
        shaped_chunks = tf_helpers.reshape_input(np.array(scaled_chunks), chunk_size)
        keys = self.key_model.predict(shaped_chunks, verbose=0)
        # Shape of keys:
        # (chunk count, chunk size, 1)

        # The model puts out a key for every iteration through the data, and (on average)
        # gets more accurate every time, so the best key is the last one:
        best_keys = keys[:, chunk_size-1, :]

        # We have the best key from each chunk, so pick the middle one:
        key = np.median(best_keys)
        return int(round(key))