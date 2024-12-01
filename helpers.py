# This file contains reusable functions that aren't necessarily well scoped

import numpy as np
import db_connect

# Read a text file in the format needed for this project
def read_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8', newline='\n') as readable:
        content = readable.read()
    return content

# Write a text file, preserving format as needed for this project
def write_text_file(text: str, path: str):
    with open(path, "w", encoding='utf-8', newline='\n') as text_file:
        text_file.write(text)

# Break a list of values into chunks.
# If the length is not evenly divisible by chunk_size, the final chunk
# will overlap the previous one so the whole thing gets converted.
def chunkify(inputs: list, chunk_size: int) -> list[list]:
    if len(inputs) < chunk_size:
        raise Exception(f"Chunk size ({chunk_size}) must be no greater than input length ({len(inputs)})")

    chunks = []

    offset = 0
    while offset < len(inputs):
        if (offset + chunk_size >= len(inputs)):
            offset = len(inputs) - chunk_size
        
        chunk = inputs[offset : offset + chunk_size]
        chunks.append(chunk)

        offset += chunk_size     
        
    return chunks

# Convert a string to a list of lists of numbers, broken up into chunks.
# If the length is not evenly divisible by chunk_size, the final chunk
# will overlap the previous one so the whole string gets converted.
# !!! If I still need this function at all, leverage the chunkify(function)
def string_to_bytes(text, chunk_size, array_out=True) -> list[list]:
    if len(text) < chunk_size:
        raise Exception(f"Chunk size ({chunk_size}) must be no greater than text length ({len(text)})")

    chunks = []

    offset = 0
    while offset < len(text):
        if (offset + chunk_size >= len(text)):
            offset = len(text) - chunk_size
        
        # I'm sure there is a more optimal way to do this...
        encoded = text[offset : offset + chunk_size].encode('UTF-8')
        if array_out:
            #!!! Describe / clean up how this make better data types for TF
            numbered = np.array([float(b) for b in encoded])
        else:
            numbered = [b for b in encoded]

        if len(encoded) != chunk_size or len(numbered) != chunk_size:
            raise Exception(f"Conversion chunk size error: {len(text)}, {len(encoded)}, {len(numbered)}, {chunk_size}")
        chunks.append(numbered)

        offset += chunk_size     
        
    return chunks


# Convert a set of numbers, in chunks as from string_to_bytes(), to a single string.
# The values will be rounded -- it is expected that the are floating-point outputs from a model.
# Recall that characters near the end of the string may be redundant.
# !!! Correct for chunk overlap, if correct final length can be known
def bytes_to_string(chunks: list[list]) -> str:
    flat_floats = [f for fs in chunks for f in fs]
    flat_bytes = [max(min(round(f), 255), 1) for f in flat_floats]
    result = "".join(chr(b) for b in flat_bytes)
    return result


def self_test():
    TEST_CHUNK_SIZE = 2

    TEST_STR = "ABCDEFG"
    GOOD_STR_CHUNKS = ['AB', 'CD', 'EF', 'FG']

    TEST_VALS = [0, 1, 2, 3, 4, 5, 6, 7]
    GOOD_VAL_CHUNKS = [[0,1], [2,3], [4,5], [6,7]]

    chunks = chunkify(TEST_STR, TEST_CHUNK_SIZE)
    print(f"Chunkify String: {chunks == GOOD_STR_CHUNKS}")

    chunks = chunkify(TEST_VALS, TEST_CHUNK_SIZE)
    print(f"Chunkify Values: {chunks == GOOD_VAL_CHUNKS}")

if __name__ == '__main__':
    self_test()