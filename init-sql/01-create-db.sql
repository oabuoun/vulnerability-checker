CREATE DATABASE pw_user_db;
USE pw_user_db;
CREATE TABLE `pw_user_db`.`user_info` (`user_id` INT NOT NULL AUTO_INCREMENT, `username` VARCHAR(50), `password` VARCHAR(75), `salt` VARCHAR(50), `FirstName` VARCHAR(50) NOT NULL, `LastName` VARCHAR(50), `BirthYear` INT, `Manager` TINYINT(1) NOT NULL DEFAULT 0, PRIMARY KEY (`user_id`));
INSERT INTO `pw_user_db`.`user_info` (`username`, `password`, `salt`, `FirstName`, `LastName`,`BirthYear`,`Manager`) VALUES ('admin', '9e2f9148f634fae1a0528b88cf9a5b373e7995011b6d1eec1fdb52a594bb962c', 'aG84TTRpOGpvMzEyTzlN','Admin','Adminsson',1970, 1);
CREATE TABLE `pw_user_db`.`user_info` (`user_id` INT NOT NULL AUTO_INCREMENT, `username` VARCHAR(50), `password` VARCHAR(50), `FirstName` VARCHAR(50) NOT NULL, `LastName` VARCHAR(50), `BirthYear` INT, `Manager` TINYINT(1) NOT NULL DEFAULT 0, PRIMARY KEY (`user_id`));
CREATE TABLE `pw_user_db`.`common_passwords` (`commonpass_id` INT AUTO_INCREMENT, `password` VARCHAR(50), PRIMARY KEY (`commonpass_id`));
CREATE TABLE `pw_user_db`.`token_table` (`token_id` INT NOT NULL AUTO_INCREMENT,`username` VARCHAR(50),`user_agent` VARCHAR(100),`token` VARCHAR(300), PRIMARY KEY (`token-id`));)
