import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import credentials

class DB(object):
    def __init__(self, creds: credentials.DB_Credentials):
        # SQL Alchemy connection info
        self.creds = creds
        self.engine = sqlalchemy.create_engine(
            f"postgresql://{creds.user}:{creds.password}@{creds.server}:{creds.port}/{creds.db_name}")

        base = sqlalchemy.ext.automap.automap_base()
        base.prepare(autoload_with=self.engine)

        # SQL Alchemy table references, auto-mapped
        self.db_ciphers_tbl = base.classes.cipher_names
        self.db_key_types_tbl = base.classes.key_types
        self.db_keys_tbl = base.classes.keys
        self.db_sources_tbl = base.classes.sources
        self.db_files_tbl = base.classes.files

    # Get a database session to allow operations.
    # Caller is responsible for closing the session.
    def get_session(self):
        return sqlalchemy.orm.Session(self.engine)


    # Returns the database ID for specified cipher name, or -1 if not found
    def get_cipher_id(self, session, name):
        results = session.query(
            self.db_ciphers_tbl.id, self.db_ciphers_tbl.name
        ).filter(self.db_ciphers_tbl.name == name).all()

        if len(results) == 0:
            return -1
        else:
            return results[0].id
        
    # Add a new cipher name to the database
    def add_cipher(self, session, name):
        session.add(self.db_ciphers_tbl(name = name))
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


    # Returns the database ID for specified source, or -1 if not found
    def get_source_by_title(self, session, title):
        results = session.query(
            self.db_sources_tbl.id
        ).filter(self.db_sources_tbl.title == title).all()

        if len(results) == 0:
            return -1
        else:
            return results[0].id

    # Add a new key type to the database
    def add_source(self, session, title, url):
        session.add(self.db_sources_tbl(title=title, url=url))
        session.commit()
