-- This file contains the SQL commands to create all tables
-- I should probably have tables for titles and urls too
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS sources;
DROP TABLE IF EXISTS keys;
DROP TABLE IF EXISTS key_types;
DROP TABLE IF EXISTS cypher_names;

CREATE TABLE cypher_names (
    id INT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE key_types (
    id INT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE keys (
    id INT PRIMARY KEY,
    key_type_id INT NOT NULL,
    FOREIGN KEY (key_type) REFERENCES key_types(id),
    value VARCHAR NOT NULL
);

CREATE TABLE sources (
    id INT PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    url VARCHAR(128) NOT NULL
);

CREATE TABLE files (
    id INT PRIMARY KEY,
    source_ID INT NOT NULL,
    FOREIGN KEY (source_ID) REFERENCES sources(id),
    cypher_ID INT NOT NULL,
    FOREIGN KEY (cypher_ID) REFERENCES cypher_names(id),
    key_ID INT,
    FOREIGN KEY (key_ID) REFERENCES keys(id),
    path VARCHAR(128)
);