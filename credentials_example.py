# This file is not used directly, it is just an example showing how to specify database credentials.
# You should create a file named credentials.py, structured just like this, with your connection info.

class DB_Credentials(object):
    pass

CONNECTION_INFO = DB_Credentials()
CONNECTION_INFO.server = "localhost"
CONNECTION_INFO.port = 5432
CONNECTION_INFO.user = "postgres"
CONNECTION_INFO.password = "THIS_IS_NOT_MY_PASSWORD"
CONNECTION_INFO.db_name = "codebreaker"
