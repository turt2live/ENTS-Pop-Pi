CREATE DATABASE pop_PI;

 CREATE USER 'popPI'@'localhost' IDENTIFIED BY 'pi';

GRANT ALL PRIVILEGES ON pop_PI TO 'popPI'@'localhost'
        WITH GRANT OPTION;

use pop_PI;

CREATE TABLE MemberAccount (Id int PRIMARY KEY AUTO_INCREMENT,RFID VARCHAR(20), Account INT, Email VARCHAR(250));
