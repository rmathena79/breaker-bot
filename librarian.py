import os
import shutil
import re # for regex
import random

import encoders
import db_connect
import helpers

from credentials import CONNECTION_INFO
from constants import *

# During development, it's very helpful to be able to run the full librarian even
# if the database already has an entry.
ABORT_ON_DB_POPULATED = True

# How many times to encrypt each file
# It might be helpful to vary this by cipher type, since the more complex ones have far more possible keys
ENCRYPTIONS_PER_SOURCE = int(len(encoders.CHARSET) * 2 // 3)

# What portion of source files to mark "test only", meaning they should never be used for training.
# That flag is propogated to encoded files based on each source.
SOURCE_TEST_ONLY_CHANCE = 0.10

# Database access wrapper
db = db_connect.DB(CONNECTION_INFO)

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
        content = helpers.read_text_file(intake_path)

        # Check that the contents look right. If not, print a message and move on to the next file.
        if not encoders.PG_FIRST_LINE_START in content:
            # It would be nice to use content.startswith(), but there can be extra unprintable bytes
            print("WARNING: Does not contain the expected first line")
            continue
        if not encoders.PG_START_CONTENT in content:
            print("WARNING: Does not contain the introductory boilerplate marker")
            continue
        if not encoders.PG_END_CONTENT in content:
            print("WARNING: Does not contain the closing boilerplate marker")
            continue

        # Find the title
        title_matches = re.search(f'{encoders.PG_FIRST_LINE_START}(.*)', content) # Note .* ends on newline
        if title_matches:
            title = title_matches.group(1)
            print(f"Title: {title}")
        else:
            print("WARNING: Could not find title")
            continue

        # Check whether this book is already in the database
        with db.get_session() as session:
            source_id = db.get_source_id_by_title(session, title)
            
            if source_id == -1:
                # Book not found in the database. Figure out the rest of the properties
                # needed to add it.

                # Try to find the eBook ID, which we need for the URL.
                # It should look like this: [eBook #12655]
                id_matches = re.search('\[eBook #(.*)\]', content)
                if id_matches:
                    ebook_id = id_matches.group(1)
                    print(f"eBook ID: {ebook_id}")
                else:
                    print("WARNING: Could not find eBook ID")
                    continue

                # Url is just based on eBook ID
                url = f"https://www.gutenberg.org/ebooks/{ebook_id}"
                print(f"url: {url}")

                # test_only flag is assigned randomly
                test_only = random.random() < SOURCE_TEST_ONLY_CHANCE
                print(f"test_only: {test_only}")

                print(f'Adding source "{title}" to database')
                db.add_source(session, title, url, test_only)
                source_id = db.get_source_id_by_title(session, title)
            else:
                print("Title is already in the database")
                if ABORT_ON_DB_POPULATED:
                    continue                

            # In normal operation, you shouldn't need to copy any files if the source is already
            # in the database. But when I'm manually trying things out, I often want them re-
            # copied, so do so here.

            # Copy the file to the raw directory
            raw_path = os.path.join(DATA_RAW_DIR, file)
            print(f"Copying file {intake_path} -> {raw_path}")
            shutil.copyfile(intake_path, raw_path)

            # Add the raw file to the database, with the test_only flag from the source
            source = db.get_source_by_id(session, source_id)            
            raw_id = encoder_ids[encoders.ENCODER_NONE]
            if len(db.get_files_by_source_and_encoder(session, source_id, raw_id)) == 0:
                db.add_file(session, source_id, raw_id, key_id=None, path=raw_path, test_only=source.test_only)
            else:
                # This really shouldn't happen
                print("WARNING: Raw file is already in the database")
                if ABORT_ON_DB_POPULATED:
                    continue


# Simplify any raw files that need it
def simplify_raw_files():
    with db.get_session() as session:
        # Get all raw files
        files = db.get_files_by_source_and_encoder(session, -1, encoder_ids[encoders.ENCODER_NONE])

        for rawfile in files:
            print(f"Raw file ID {rawfile.id}")

            # Check whether we've already simplified this file
            simple_files = db.get_files_by_source_and_encoder(session, rawfile.source_id, encoder_ids[encoders.ENCODER_SIMPLIFIER])
            if len(simple_files) > 0:
                print("File already simplified")
                if ABORT_ON_DB_POPULATED:
                    continue

            # Read the whole file as a string
            raw = helpers.read_text_file(rawfile.path)

            # Simplify it
            print("Simplifying")
            simplified = encoders.encode_simple(raw)

            # Retain the original filename for easier reference
            filename = os.path.basename(rawfile.path)

            # Add the simplified file to the database
            print("Adding simplified file to database")
            simplified_path = os.path.join(DATA_SIMPLIFIED_DIR, filename)
            db.add_file(session, rawfile.source_id, encoder_ids[encoders.ENCODER_SIMPLIFIER], None, simplified_path, rawfile.test_only)

            # Save to the simplified data directory
            print(f"Saving to {simplified_path}")
            helpers.write_text_file(simplified, simplified_path)

def encrypt_simple_files():      
    with db.get_session() as session:
        # Get all simplified (plaintext) files
        files = db.get_files_by_source_and_encoder(session, -1, encoder_ids[encoders.ENCODER_SIMPLIFIER])

        for plainfile in files:
            print(f"Plaintext file ID {plainfile.id}")

            for cipher_name in encoders.AVAILABLE_CIPHERS:
                if cipher_name == encoders.ENCODER_CAESAR:
                    key_type_id = key_type_ids[encoders.KEY_NAME_CAESAR]
                    func_get_key = encoders.get_key_caesar
                    func_encode = encoders.encode_caesar
                    func_decode = encoders.decode_caesar
                elif cipher_name == encoders.ENCODER_SUBST:
                    key_type_id = key_type_ids[encoders.KEY_NAME_SUBST]
                    func_get_key = encoders.get_key_substitution
                    func_encode = encoders.encode_substitution
                    func_decode = encoders.decode_substitution
                else:
                    raise Exception(f"Unknown cipher {cipher_name}")

                # Check whether we've already encrypted this file with this cipher
                encoder_id = encoder_ids[cipher_name]
                encrypted_files = db.get_files_by_source_and_encoder(session, plainfile.source_id, encoder_id)
                if len(encrypted_files) >= ENCRYPTIONS_PER_SOURCE:
                    print(f'File already encrypted with "{cipher_name}" {len(encrypted_files)} times (max {ENCRYPTIONS_PER_SOURCE})')
                    if ABORT_ON_DB_POPULATED:
                        continue
                times_to_encrypt = ENCRYPTIONS_PER_SOURCE - len(encrypted_files)

                # Read the whole file as a string
                plaintext = helpers.read_text_file(plainfile.path)

                # We're going to encrypt multiple times, and each time we should use a different key,
                # so we need to track which ones we've used.
                keys_used = []
                for i in range(times_to_encrypt):
                    # Find a key we haven't used yet for this file
                    good_key = False
                    while not good_key:
                        key = func_get_key()
                        good_key = not key in keys_used
                        if not good_key:
                            print(f"Key {key} already used -- try again")
                    keys_used.append(key)

                    # Encrypt it, and make sure decryption works
                    print(f"Encrypting with {cipher_name}")
                    cipher_text = func_encode(plaintext, key)
                    deciphered_text = func_decode(cipher_text, key)

                    if deciphered_text != plaintext:
                        raise Exception(f'Decrypted text did not match plaintext for cipher "{cipher_name}", key "{key}"')                

                    # Add the key to the database, or just get its ID if it's already there
                    # (there's only so many possible keys, espescially for simpler ciphers)
                    key_id = db.get_key_id_by_type_and_value(session, key_type_id, str(key))
                    if key_id == -1:
                        print("Adding key to database")
                        db.add_key(session, key_type_id, str(key))
                        key_id = db.get_key_id_by_type_and_value(session, key_type_id, str(key))
                    print(f"Key ID {key_id}")

                    # Pick a filename based on database IDs for source, encoder, and key
                    filename = f"{plainfile.source_id:08}_{encoder_id:08}_{key_id:08}.txt"
                    encrypted_path = os.path.join(DATA_ENCODED_DIR, filename)

                    # Add the simplified file to the database
                    print("Adding encrypted file to database")
                    db.add_file(session, plainfile.source_id, encoder_id, key_id, encrypted_path, plainfile.test_only)

                    # Save to the encrypted data directory 
                    print(f"Saving to {encrypted_path}")
                    helpers.write_text_file(cipher_text, encrypted_path)

def main():
    prep_dirs()
    prep_db()
    process_intake()
    simplify_raw_files()
    encrypt_simple_files()

if __name__ == '__main__':
    main()