CREATE DATABASE `baselessdata_db`;

CREATE DATABASE #DB;

CREATE TABLE IF NOT Exists #DB.tbl_user (
    email VARCHAR(100),
    password_hash VARCHAR(256),
    PRIMARY KEY(email)

CREATE TABLE IF NOT Exists `baselessdata_db`.tbl_user (
    email varchar(100),
    password_hash varchar(256),
    primary key(email)
    );

CREATE TABLE IF NOT EXISTS favorite(
	EMAIL VARCHAR(255),
	COURSE_ID VARCHAR(255)
);


USE `baselessdata_db`;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(256)
)
BEGIN
    if ( select exists (select 1 from tbl_user where email = p_email) ) THEN
        select 'Username Exists !!';
    ELSE
        insert into tbl_user (
            email,
            password_hash
        )
        values (
            p_email,
            p_password
        );
    END IF;
END$$
DELIMITER ;
