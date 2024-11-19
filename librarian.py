import os
import shutil
import re # for regex
import encoders
import db_connect

from credentials import SAMPLE_DB, FULL_DB

# These need to be shared with the model maker and easier to customize
SAMPLE_DATA_DIR = "sample_data"
FULL_DATA_DIR = "full_data"
DATA_DIR = SAMPLE_DATA_DIR
DATA_INTAKE_DIR = os.path.join(DATA_DIR, "intake")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_SIMPLIFIED_DIR = os.path.join(DATA_DIR, "simplified")
DATA_ENCODED_DIR = os.path.join(DATA_DIR, "encoded")

db = db_connect.DB(SAMPLE_DB)

# Key strings for making sense of Project Gutenberg texts:
#!!! I have not confirmed that these are universal
PG_FIRST_LINE_START = "The Project Gutenberg eBook of "
PG_START_CONTENT = "*** START OF THE PROJECT GUTENBERG EBOOK "
PG_END_CONTENT = "*** END OF THE PROJECT GUTENBERG EBOOK "
PG_SENTINEL_LINE_END = " ***"

# Database IDs, name: ID
encoder_ids= {}
key_type_ids = {}


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


# Initialize database content, adding encoder and key types if needed,
# and getting their ID numbers. Also initializes the SQL Alchemy engine object
# and tables references by auto-mapping.
def prep_db():
    # Get database IDs for encoders and key types, adding them to the db if needed
    with db.get_session() as session:
        for encoder in encoders.ALL_ENCODER_NAMES:
            id = db.get_encoder_id(session, encoder)
            if (id == -1):
                print(f'Adding encoder "{encoder}" to database')
                db.add_encoder(session, encoder)
                id = db.get_encoder_id(session, encoder)

            encoder_ids[encoder] = id

        print(f"Encoder IDs: {encoder_ids}")

        for key_type in encoders.KEY_NAMES:
            id = db.get_key_type_id(session, key_type)
            if (id == -1):
                print(f'Adding key type "{key_type}" to database')
                db.add_key_type(session, key_type)
                id = db.get_key_type_id(session, key_type)

            key_type_ids[key_type] = id

        print(f"Key Type IDs: {key_type_ids}")


# Process all files in the intake directory:
#
# 1) Read the file to ensure it is usable, which for now means it is a text file from Project Gutenberg
# 2) Determine the title and URL, based on file content
# 3) Add the source text to the database
# 4) Copy the file to the "raw" directory 
#    (note copy, not move, to avoid confusion with the checked-in sample data)
# 5) Add the raw file location to the database
def process_intake():
    files = [f for f in os.listdir(DATA_INTAKE_DIR) if os.path.isfile(os.path.join(DATA_INTAKE_DIR, f))]
    print(f"Processing intake directory {DATA_INTAKE_DIR}: {len(files)} files")

    # Handle each file
    for file in files:
        print(f"{file}:")
        intake_path = os.path.join(DATA_INTAKE_DIR, file)

        # Read the whole file as a string
        with open(intake_path, 'r', encoding='utf-8') as readable:
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
        with db.get_session() as session:
            source_id = db.get_source_id_by_title(session, title)
            
            if source_id == -1:
                # Add this book to the database
                print(f'Adding source "{title}" to database')
                db.add_source(session, title, url)
                source_id = db.get_source_id_by_title(session, title)
            else:
                print("Title is already in the database")
                continue                

            # Copy the file to the raw directory
            raw_path = os.path.join(DATA_RAW_DIR, file)
            print(f"Copying file {intake_path} -> {raw_path}")
            shutil.copyfile(intake_path, raw_path)

            # Add the raw file to the database
            raw_id = encoder_ids[encoders.ENCODER_NONE]
            if db.get_file_by_source_and_encoder(session, source_id, raw_id) == None:
                db.add_file(session, source_id, raw_id, key_id=None, path=raw_path)
            else:
                print("WARNING: Raw file is already in the database")
                continue


# Simplify any raw files that need it
def simplify_raw_files():
    pass


def main():
    prep_dirs()
    prep_db()
    process_intake()
    simplify_raw_files()

main()