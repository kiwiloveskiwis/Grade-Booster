USE baselessdata_db;

SHOW TABLES;
DESCRIBE name_of_table;

CREATE TABLE user_fac (
    email VARCHAR(100),
    subject VARCHAR(256),
    number INT,
    PRIMARY KEY(email)