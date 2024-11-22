# This file contains reusable functions that aren't necessarily well scoped

import numpy as np

# Read a text file in the format needed for this project
def read_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8', newline='\n') as readable:
        content = readable.read()
    return content

# Write a text file, preserving format as needed for this project
def write_text_file(text: str, path: str):
    with open(path, "w", encoding='utf-8', newline='\n') as text_file:
        text_file.write(text)

# Convert a string to a list of lists of numbers, broken up into chunks.
# If the length is not evenly divisible by chunk_size, the final chunk
# will overlap the previous one so the whole string gets converted.
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
def bytes_to_string(chunks: list[list]) -> str:
    flat_floats = [f for fs in chunks for f in fs]
    flat_bytes = [max(min(round(f), 255), 1) for f in flat_floats]
    result = "".join(chr(b) for b in flat_bytes)
    return result
