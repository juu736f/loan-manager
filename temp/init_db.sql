create database `loans_db`;
use `loans_db`;
CREATE TABLE `customers` (
    `CustomerID` INT AUTO_INCREMENT PRIMARY KEY,
    `LastName` VARCHAR(256),
    `FirstName` VARCHAR(256),
    `Email` VARCHAR(256),
    `Telephone` VARCHAR(256)
);
ALTER TABLE `customers` ADD UNIQUE(`CustomerID`);

CREATE TABLE `devices` (
    `DeviceID` INT AUTO_INCREMENT PRIMARY KEY,
    `DeviceName` VARCHAR(512),
    `DeviceType` VARCHAR(256),
    `LoanStatus` BOOL
);
ALTER TABLE `devices` ADD UNIQUE(`DeviceID`);

CREATE TABLE `loans` (
    `LoanID` INT AUTO_INCREMENT PRIMARY KEY,
    `CustomerID` INT,
    `DeviceID` INT,
    `LoanStart` DATE,
    `LoanEnd` DATE
);
ALTER TABLE `loans` ADD UNIQUE(`LoanID`); 
ALTER TABLE `loans` ADD CONSTRAINT `fk_customerid` FOREIGN KEY (`CustomerID`) REFERENCES customers(CustomerID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `loans` ADD CONSTRAINT `fk_deviceid` FOREIGN KEY (`DeviceID`) REFERENCES devices(DeviceID) ON DELETE CASCADE ON UPDATE CASCADE; 

