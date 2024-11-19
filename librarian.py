import os
import re # for regex
from credentials import SAMPLE_DB, FULL_DB
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import encoders

# These need to be shared with the model maker and easier to customize
SAMPLE_DATA_DIR = "sample_data"
FULL_DATA_DIR = "full_data"
DATA_DIR = SAMPLE_DATA_DIR
DATA_INTAKE_DIR = os.path.join(DATA_DIR, "intake")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_SIMPLIFIED_DIR = os.path.join(DATA_DIR, "simplified")
DATA_ENCODED_DIR = os.path.join(DATA_DIR, "encoded")

# SQL Alchemy connection info
db_credentials = SAMPLE_DB
db_engine = None

# SQL Alchemy table references, auto-mapped
db_ciphers_tbl = None
db_key_types_tbl = None
db_keys_tbl = None
db_sources_tbl = None
db_files_tbl = None

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

# Returns the database ID for specified cipher name, or -1 if not found
def get_cipher_id(name, session):
    results = session.query(
        db_ciphers_tbl.id, db_ciphers_tbl.name
    ).filter(db_ciphers_tbl.name == name).all()

    if len(results) == 0:
        return -1
    else:
        return results[0].id
    
# Returns the database ID for specified key type, or -1 if not found
def get_key_type_id(name, session):
    results = session.query(
        db_key_types_tbl.id, db_key_types_tbl.name
    ).filter(db_key_types_tbl.name == name).all()

    if len(results) == 0:
        return -1
    else:
        return results[0].id    

# Initialize database content, adding encoder and key types if needed,
# and getting their ID numbers. Also initializes the SQL Alchemy engine object
# and tables references by auto-mapping.
def prep_db():
    global db_engine
    db_engine = sqlalchemy.create_engine(
        f"postgresql://{db_credentials.user}:{db_credentials.password}@{db_credentials.server}:{db_credentials.port}/{db_credentials.db_name}")
    
    # reflect an existing database into a new model
    base = sqlalchemy.ext.automap.automap_base()
    base.prepare(autoload_with=db_engine)

    # populate table references
    global db_ciphers_tbl
    global db_key_types_tbl
    global db_keys_tbl
    global db_sources_tbl
    global db_files_tbl

    db_ciphers_tbl = base.classes.cipher_names
    db_key_types_tbl = base.classes.key_types
    db_keys_tbl = base.classes.keys
    db_sources_tbl = base.classes.sources
    db_files_tbl = base.classes.files

    # Get database IDs for encoders and key types, adding them to the db if needed
    with sqlalchemy.orm.Session(db_engine) as session:
        for encoder in encoders.ENCODER_NAMES:
            id = get_cipher_id(encoder, session)
            if (id == -1):
                print(f'Adding encoder "{encoder}" to database')
                session.add(db_ciphers_tbl(name = encoder))
                session.commit()

                id = get_cipher_id(encoder, session)

            encoder_ids[encoder] = id

        print(f"Encoder IDs: {encoder_ids}")

        for key_type in encoders.KEY_NAMES:
            id = get_key_type_id(key_type, session)
            if (id == -1):
                print(f'Adding key type "{key_type}" to database')
                session.add(db_key_types_tbl(name = key_type))
                session.commit()

                id = get_key_type_id(key_type, session)

            key_type_ids[key_type] = id

        print(f"Key Type IDs: {key_type_ids}")
                   



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
    prep_db()
    process_intake()

main()