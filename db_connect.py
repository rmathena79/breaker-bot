import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import pathlib
import random
import numpy as np

import credentials
import encoders
import helpers

class DB(object):
    def __init__(self, creds: credentials.DB_Credentials):
        # SQL Alchemy connection info
        self.creds = creds
        self.engine = sqlalchemy.create_engine(
            f"postgresql://{creds.user}:{creds.password}@{creds.server}:{creds.port}/{creds.db_name}")

        base = sqlalchemy.ext.automap.automap_base()
        base.prepare(autoload_with=self.engine)

        # SQL Alchemy table references, auto-mapped
        self.db_encoder_tbl = base.classes.encoder_names
        self.db_key_types_tbl = base.classes.key_types
        self.db_keys_tbl = base.classes.cipher_keys
        self.db_sources_tbl = base.classes.sources
        self.db_files_tbl = base.classes.files

    # Get a database session to allow operations.
    # Caller is responsible for closing the session.
    def get_session(self):
        return sqlalchemy.orm.Session(self.engine)
    
    # Convenience method to get encoder and key type ID maps
    # Returns a tuple: (encoder_ids, key_type_ids)
    # Each is a map from ID number to name
    def get_id_maps(self, session):
        encoder_ids= {}
        key_type_ids = {}

        for encoder in encoders.ALL_ENCODER_NAMES:
            id = self.get_encoder_id(session, encoder)
            encoder_ids[encoder] = id
        for key_type in encoders.KEY_NAMES:
            id = self.get_key_type_id(session, key_type)
            key_type_ids[key_type] = id

        return (encoder_ids, key_type_ids)
    
    # Convenience method to get maps from source IDs to corresponding plaintext and ciphertext files.
    # Returns a tuple: (source_id_to_plaintext, source_id_to_ciphertext)
    # Each is a map from source ID to file ID. The plaintext file ID is a single value, the ciphertext is a list.
    def get_source_maps(self, session, max_encrypted_files, cipher_id, test_only):

        source_id_to_plaintext = {}
        source_id_to_ciphertext = {}

        encrypted_files = self.get_files_by_source_and_encoder(session, -1, cipher_id, test_only=test_only)
        simplifier_encoder_id = self.get_encoder_id(session, encoders.ENCODER_SIMPLIFIER)

        if len(encrypted_files) > max_encrypted_files and max_encrypted_files > 0:
            encrypted_files = random.sample(encrypted_files, max_encrypted_files)

        for c in encrypted_files:
            sid = c.source_id
        
            if sid not in source_id_to_plaintext:
                plaintext_ids = self.get_files_by_source_and_encoder(session, sid, simplifier_encoder_id, test_only=test_only)
                if len(plaintext_ids) != 1:
                    raise Exception(f"Found {len(plaintext_ids)} plaintexts for source ID {sid}; should be exactly 1")
                source_id_to_plaintext[sid] = plaintext_ids[0]

            if sid not in source_id_to_ciphertext:
                source_id_to_ciphertext[sid] = []
            source_id_to_ciphertext[sid].append(c)

        return (source_id_to_plaintext, source_id_to_ciphertext)
    
    # Convenience method to get features and targets (X and y) formatted for use.
    # Returns a tuple: (X, y_keys, y_texts)
    #   X is a list of lists, where the inner list is chunks of ciphertext, as offsets
    #   y_keys is a list of keys, where key structure varies by encoder type (floats for Caesar)
    #   y_texts is a list of lists, where the inner list is chunks of plaintext, as offsets
    def get_features_and_targets(self, session, source_id_to_plaintext: dict, source_id_to_ciphertext: dict, encoder: str, chunk_size: int,
                                 want_keys = True, want_texts = True) -> tuple:
        X = []
        y_keys = []
        y_texts = []

        for sid in source_id_to_plaintext:
            if want_texts:
                plaintext = helpers.read_text_file(source_id_to_plaintext[sid].path)
                plaintext_offsets = encoders.string_to_offsets(plaintext)
                plaintext_offset_chunks = helpers.chunkify(plaintext_offsets, chunk_size)    

            for c in source_id_to_ciphertext[sid]:
                ciphertext = helpers.read_text_file(c.path)
                ciphertext_offsets = encoders.string_to_offsets(ciphertext)
                ciphertext_offset_chunks = helpers.chunkify(ciphertext_offsets, chunk_size)

                if want_keys:
                    if encoder == encoders.ENCODER_CAESAR:
                        key_value = float(self.get_key_by_id(session, c.key_id).value)
                        
                    elif encoder == encoders.ENCODER_SUBST:
                        key_str = self.get_key_by_id(session, c.key_id).value
                        key_value_ints = encoders.string_to_offsets(key_str)
                        key_value = np.array(key_value_ints).astype(float)

                    else:
                        raise Exception(f"Unsupported encoder {encoder}")

                for i in range (len(ciphertext_offset_chunks)):
                    ciphertext_offset_chunk = ciphertext_offset_chunks[i]
                    X.append(np.array(ciphertext_offset_chunk).astype(float))

                    if want_texts: 
                        plaintext_offset_chunk = plaintext_offset_chunks[i]
                        y_texts.append(np.array(plaintext_offset_chunk).astype(float))
                    if want_keys:
                        y_keys.append(key_value)

        return X, y_keys if want_keys else None, y_texts if want_texts else None


    # Returns the database ID for specified encoder name, or -1 if not found
    def get_encoder_id(self, session, name):
        results = session.query(
            self.db_encoder_tbl.id, self.db_encoder_tbl.name
        ).filter(self.db_encoder_tbl.name == name).all()

        if len(results) == 0:
            return -1
        else:
            return results[0].id
        
    # Add a new encoder name to the database
    def add_encoder(self, session, name):
        session.add(self.db_encoder_tbl(name = name))
        session.commit()
        

    # Returns the database ID for specified key type, or -1 if not found
    def get_key_type_id(self, session, name):
        results = session.query(
            self.db_key_types_tbl.id, self.db_key_types_tbl.name
        ).filter(self.db_key_types_tbl.name == name).all()

        if len(results) == 0:
            return -1
        else:
            return results[0].id    

    # Add a new key type to the database
    def add_key_type(self, session, name):
        session.add(self.db_key_types_tbl(name = name))
        session.commit()


    # Get a single source by its ID, or None if not found
    def get_source_by_id(self, session, id):
        results = session.query(
            self.db_sources_tbl
        ).filter(
            self.db_sources_tbl.id == id
        ).all()

        if len(results) == 0:
            return None
        else:
            return results[0]
        
    # Returns the database ID for specified source, or -1 if not found
    def get_source_id_by_title(self, session, title, test_only=None):
        q = session.query(
            self.db_sources_tbl.id
        ).filter(self.db_sources_tbl.title == title)
        
        if test_only is not None:
            q = q.filter(self.db_sources_tbl.test_only == test_only)
            
        results = q.all()

        if len(results) == 0:
            return -1
        else:
            return results[0].id

    # Add a new key type to the database
    def add_source(self, session, title, url, test_only):
        session.add(self.db_sources_tbl(title=title, url=url, test_only=test_only))
        session.commit()


    # Get all files by source ID and/or encoder ID. Returns a list of database rows.
    # Specify -1 for either ID to exclude it from filtering.
    # Specify test_only as True or False to limit results accordingly,
    #    or leave it as None to ignore that property
    def get_files_by_source_and_encoder(self, session, source_id, encoder_id, test_only=None):
        q = session.query(
            self.db_files_tbl
        )

        if source_id != -1:
            q = q.filter(self.db_files_tbl.source_id == source_id)
        if encoder_id != -1:
            q = q.filter(self.db_files_tbl.encoder_id == encoder_id)
        if test_only is not None:
            q = q.filter(self.db_files_tbl.test_only == test_only)

        results = q.all()
        return results
        
    # Add a file to the database.
    # Note key_id can be None, for raw files, but all other parameters must be filled
    def add_file(self, session, source_id, encoder_id, key_id, path, test_only):
        new_row = self.db_files_tbl(
            source_id = source_id,
            encoder_id = encoder_id,
            key_id = key_id,
            path = pathlib.Path(path).as_posix(),
            test_only = test_only)
        session.add(new_row)
        session.commit()

       
    # Get a single key by its ID, or None if not found
    def get_key_by_id(self, session, key_id):
        results = session.query(
            self.db_keys_tbl
        ).filter(
            self.db_keys_tbl.id == key_id
        ).all()

        if len(results) == 0:
            return None
        else:
            return results[0]

    # Returns the database ID for specified key, or -1 if not found
    def get_key_id_by_type_and_value(self, session, key_type_id, key_value: str):
        results = session.query(
            self.db_keys_tbl.id
        ).filter(
            self.db_keys_tbl.key_type_id == key_type_id,
            self.db_keys_tbl.value == key_value
        ).all()

        if len(results) == 0:
            return -1
        else:
            return results[0].id
        
    def add_key(self, session, key_type_id, key_value:str):
        session.add(self.db_keys_tbl(key_type_id = key_type_id, value = key_value))
        session.commit()
