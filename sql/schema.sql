-- This file contains the SQL commands to create all tables
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS sources;
DROP TABLE IF EXISTS cipher_keys;
DROP TABLE IF EXISTS key_types;
DROP TABLE IF EXISTS encoder_names;

CREATE TABLE encoder_names (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE key_types (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(128) NOT NULL
);

-- Naming this table "keys" apparently conflicted with some reserved word,
-- leading to VERY unhelpful error messages.
CREATE TABLE cipher_keys (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    key_type_id INT NOT NULL,
    FOREIGN KEY (key_type_id) REFERENCES key_types(id),
    value VARCHAR NOT NULL
);

CREATE TABLE sources (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR NOT NULL,
    url VARCHAR(256) NOT NULL,
    test_only BOOLEAN NOT NULL
);

CREATE TABLE files (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    source_ID INT NOT NULL,
    FOREIGN KEY (source_ID) REFERENCES sources(id),
    encoder_ID INT NOT NULL,
    FOREIGN KEY (encoder_ID) REFERENCES encoder_names(id),
    key_ID INT,
    FOREIGN KEY (key_ID) REFERENCES cipher_keys(id),
    path VARCHAR(128) NOT NULL,
    test_only BOOLEAN NOT NULL
);