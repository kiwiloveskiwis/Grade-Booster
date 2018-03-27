CREATE DATABASE `baselessdata_db`;

CREATE TABLE IF NOT Exists `baselessdata_db`.tbl_user (
    email VARCHAR(100),
    password_hash VARCHAR(255),
    PRIMARY KEY(email)

CREATE TABLE IF NOT EXISTS `baselessdata_db`.favorite(
	EMAIL VARCHAR(255),
	COURSE_SUB VARCHAR(255),
    COURSE_NUM int(11) 
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
