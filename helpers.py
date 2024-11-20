# This file contains reusable functions that aren't necessarily well scoped

# Read a text file in the format needed for this project
def read_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8', newline='\n') as readable:
        content = readable.read()
    return content

# Write a text file, preserving format as needed for this project
def write_text_file(text: str, path: str):
    with open(path, "w", encoding='utf-8', newline='\n') as text_file:
        text_file.write(text)
