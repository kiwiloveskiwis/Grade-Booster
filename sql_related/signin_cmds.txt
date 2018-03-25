CREATE DATABASE `baselessdata_db`;

CREATE TABLE `baselessdata_db`.tbl_user (
    email varchar(100),
    password_hash varchar(256),
    primary key(email)
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