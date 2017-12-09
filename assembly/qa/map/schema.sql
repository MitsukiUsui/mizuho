CREATE TABLE read
(
    id INTEGER PRIMARY KEY,
    name TEXT
);
CREATE TABLE scaffold
(
    id INTEGER PRIMARY KEY,
    name TEXT,
    length INTEGER
);
CREATE TABLE bowtie
(
    read_id INTEGER,
    scaff_id INTEGER
);
CREATE TABLE bwa
(
    read_id INTEGER,
    scaff_id INTEGER
);
.exit
