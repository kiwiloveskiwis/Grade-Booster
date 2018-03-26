CREATE DATABASE `baselessdata_db`;

<<<<<<< HEAD:sql_cmds.txt
CREATE DATABASE #DB;

CREATE TABLE #DB.tbl_user (
    email VARCHAR(100),
    password_hash VARCHAR(256),
    PRIMARY KEY(email)
=======
CREATE TABLE `baselessdata_db`.tbl_user (
    email varchar(100),
    password_hash varchar(256),
    primary key(email)
>>>>>>> refs/remotes/origin/master:sql_related/signin_cmds.txt
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