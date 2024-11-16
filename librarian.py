import os
import re

# These need to be shared with the model maker and easier to customize
DATA_DIR = "sample_data"
DATA_INTAKE_DIR = os.path.join(DATA_DIR, "intake")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_SIMPLIFIED_DIR = os.path.join(DATA_DIR, "simplified")
DATA_ENCODED_DIR = os.path.join(DATA_DIR, "encoded")

# Key strings for making sense of Project Gutenberg texts:
#!!! I have not confirmed that these are universal
PG_FIRST_LINE_START = "The Project Gutenberg eBook of "
PG_START_CONTENT = "*** START OF THE PROJECT GUTENBERG EBOOK "
PG_END_CONTENT = "*** END OF THE PROJECT GUTENBERG EBOOK "
PG_SENTINEL_LINE_END = " ***"

# Make a directory if it does not already exist.
# Does not intermediate directories.
def make_dir_if_not_exist(dir):
    if not os.path.isdir(dir):
        print(f"Creating {dir}")
        os.mkdir(dir)

# Ensure all needed data directories exist
def prep_dirs():    
    make_dir_if_not_exist(DATA_DIR)
    make_dir_if_not_exist(DATA_INTAKE_DIR)
    make_dir_if_not_exist(DATA_RAW_DIR)
    make_dir_if_not_exist(DATA_SIMPLIFIED_DIR)
    make_dir_if_not_exist(DATA_ENCODED_DIR)

# Process all files in the intake directory:
#
# 1) Read the file to ensure it is usable, which for now means it is a text file from Project Gutenberg
# 2) Determine the title and URL, based on file content
# 3) Update the database
# 4) Move the file to the "raw" directory
def process_intake():
    files = [f for f in os.listdir(DATA_INTAKE_DIR) if os.path.isfile(os.path.join(DATA_INTAKE_DIR, f))]
    print(f"Processing intake directory {DATA_INTAKE_DIR}: {len(files)} files")

    # Handle each file
    for file in files:
        print(f"{file}:")

        # Read the whole file as a string
        with open(os.path.join(DATA_INTAKE_DIR, file), 'r', encoding='utf-8') as readable:
            content = readable.read()

        # Check that the contents look right. If not, print a message and move on to the next file.
        if not PG_FIRST_LINE_START in content:
            # It would be nice to use content.startswith(), but there can be extra unprintable bytes
            print("WARNING: Does not contain the expected first line")
            continue
        if not PG_START_CONTENT in content:
            print("WARNING: Does not contain the introductory boilerplate marker")
            continue
        if not PG_END_CONTENT in content:
            print("WARNING: Does not contain the closing boilerplate marker")
            continue

        # Find the title
        title_matches = re.search(f'{PG_FIRST_LINE_START}(.*)', content) # Note .* ends on newline
        if title_matches:
            title = title_matches.group(1)
            print(f"Title: {title}")
        else:
            print("WARNING: Could not find title")
            continue

        # Try to find the eBook ID, which we need for the URL.
        # It should look like this: [eBook #12655]
        id_matches = re.search('\[eBook #(.*)\]', content)
        if id_matches:
            ebook_id = id_matches.group(1)
            print(f"eBook ID: {ebook_id}")
        else:
            print("WARNING: Could not find eBook ID")
            continue

        url = f"https://www.gutenberg.org/ebooks/{ebook_id}"
        print(f"url: {url}")

        # Check whether this book is already in the database
        # Add this book to the database
        # Confirm database entry

        # Move the file to the raw directory

        print()

def main():
    prep_dirs()
    process_intake()

main()