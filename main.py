import os
import sys
import logging as log
import argparse
import mysql.connector as sql
import random
import string
from tabulate import tabulate as tab

e = None
conn = None
workingDir = os.getcwd()
dbcredPath = os.path.join(workingDir, "dbcred")

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode (debugging)")
args = parser.parse_args()

if args.verbose:
    log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)
    log.basicConfig(level=log.DEBUG)
    log.debug("Verbose mode invoked.")
else:
    log.basicConfig(format='', level=log.CRITICAL)

def main():
    log.info("main invoked")
    global conn
    readPermission = readPermissionCheck()
    if os.path.exists(dbcredPath):
        log.info("dbcred found")
        if conn is None:
            conn = dbConn()
        dbWriteCheck()
    else:
        if readPermission == True:
            initDBcred()
        else:
            log.critical(f"Fatal error: No read permissions in directory {workingDir}")
            sys.exit(1)
   

def initDBcred():
    log.info("initDBcred invoked")
    while True:
        userInput = input("Do you want to create the database credential file? (yes/no): ")
        if userInput.lower() in ["yes", "y"]:
            log.info("User input YES to creating dbcred")
            dbcredCreate()
        elif userInput.lower() in ["no", "n"]:
            log.info("User input NO to creating dbcred")
            print("Exiting...")
            sys.exit(0)
        else:
            log.warning("Invalid input") 
            print(f"{userInput} is not a valid option (yes/no)")

def readPermissionCheck():
    if os.access(workingDir, os.R_OK):    
        log.info("Read permissions granted")
        readPermission = True
        return readPermission
    else:
        log.error("Read permissions not granted.")
        readPermission = False
        print(f"[CRITICAL] Read permissions are not granted for the directory: {workingDir}")
        sys.exit(1)
    
def writePermissionCheck():
    log.info("writePermissionCheck invoked")
    if os.access(workingDir, os.W_OK):
        log.info("Write permissions granted")
        writePermission = True
        return writePermission
    else:
        log.error("Write permissions not granted.")
        writePermission = False
        print(f"[CRITICAL] Write permissions are not granted for the directory: {workingDir}")
        sys.exit(1)

def dbcredCreate():
    global conn
    log.info("dbcredCreate invoked")
    writePermission = writePermissionCheck()
    if writePermission is True:
        dbHost = input("Insert hostname: ")
        dbPort = input("Insert port: ")
        dbUser = input("Insert username: ")
        dbPass = input("Insert password: ")
        dbData = input("Insert database: ")
        with open("dbcred", "w") as file:
            file.write(f"host='{dbHost}', port='{dbPort}', user='{dbUser}', password='{dbPass}', database='{dbData}'")
        if conn is None:
            conn = dbConn()
    else:
        log.critical(f"No write permissions for directory: {workingDir}")
    dbWriteCheck()
        
def parseCredentials():
    log.info("parseCredentials invoked")
    with open(dbcredPath) as dbcred:
        log.info(dbcred)
        credentials = dbcred.read()
        credentials = credentials.strip()
        creds_dict = {}
    for item in credentials.split(","):
        key, value = item.split("=")
        creds_dict[key.strip()] = value.strip().strip("'")
    return creds_dict
        
def dbConn():
    log.info("dbConn invoked")
    log.info("(re-)Establishing database connection")
    creds_dict = parseCredentials()
    global conn
    try:
        conn = sql.connect(
            host=creds_dict["host"],
            port=int(creds_dict["port"]),
            user=creds_dict["user"],
            password=creds_dict["password"],
            database=creds_dict["database"],
            )
    except sql.Error as e:
        log.warning(f"Database {creds_dict['database']} not found.")
        conn = sql.connect(
            host=creds_dict["host"],
            port=int(creds_dict["port"]),
            user=creds_dict["user"],
            password=creds_dict["password"],
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE `{creds_dict['database']}`")
        cursor.execute(f"USE `{creds_dict['database']}`") 
        cursor.execute("CREATE TABLE `customers` (`CustomerID` INT AUTO_INCREMENT PRIMARY KEY,`LastName` VARCHAR(256),`FirstName` VARCHAR(256),`Email` VARCHAR(256),`Telephone` VARCHAR(256))")
        cursor.execute("ALTER TABLE `customers` ADD UNIQUE(`CustomerID`)")
        cursor.execute("CREATE TABLE `devices` (`DeviceID` INT AUTO_INCREMENT PRIMARY KEY,`DeviceName` VARCHAR(512),`DeviceType` VARCHAR(256),`LoanStatus` BOOL)")
        cursor.execute("ALTER TABLE `devices` ADD UNIQUE(`DeviceID`);")
        cursor.execute("CREATE TABLE `loans` (`LoanID` INT AUTO_INCREMENT PRIMARY KEY,`CustomerID` INT,`DeviceID` INT,`LoanStart` DATE,`LoanEnd` DATE);")
        cursor.execute("ALTER TABLE `loans` ADD UNIQUE(`LoanID`);")
        cursor.execute("ALTER TABLE `loans` ADD CONSTRAINT `fk_customerid` FOREIGN KEY (`CustomerID`) REFERENCES customers(CustomerID) ON DELETE CASCADE ON UPDATE CASCADE;")
        cursor.execute("ALTER TABLE `loans` ADD CONSTRAINT `fk_deviceid` FOREIGN KEY (`DeviceID`) REFERENCES devices(DeviceID) ON DELETE CASCADE ON UPDATE CASCADE; ")
        conn.commit()
        log.info(f"Database '{creds_dict['database']}' created successfully.")
    finally:
        conn = sql.connect(
            host=creds_dict["host"],
            port=int(creds_dict["port"]),
            user=creds_dict["user"],
            password=creds_dict["password"],
            database=creds_dict["database"],
            )
    return conn

def dbConnClose():
    log.info("dbConnClose invoked")
    global conn
    if conn and conn.is_connected():
        conn.close()
        log.info("Database connection closed")

def dbWriteCheck():
    log.info("dbWriteCheck invoked")
    global conn
    randomData = randomNameGenerator()
    global rLastName
    rLastname = randomData[0]
    rFirstname = randomData[1]
    rEmail = randomData[2]
    rTelephone = randomData[3]
    cursor = conn.cursor() 
    try:
        query = "INSERT INTO `customers` (`LastName`, `FirstName`, `Email`, `Telephone`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (rLastname, rFirstname, rEmail, rTelephone))
        conn.commit()
        log.info("Data written to Database")
        dbReadCheck(rLastname, rFirstname)
    except Exception as e:
        log.critical(f"Failed to write to database: {e}")
        
        conn.close()
        sys.exit(1)


def dbReadCheck(rLastname, rFirstname):
    log.info("dbReadCheck invoked")
    global conn
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM `customers` WHERE LastName=%s"
        cursor.execute(query, (rLastname,))
        queryResult = cursor.fetchall()
        log.info(queryResult)
        headers = ['ID', 'Last Name', 'First Name', 'Email', 'Phone']
        print(tab(queryResult, headers=headers, tablefmt='grid'))
        dbUpdateCheck(rLastname, rFirstname)
    except Exception as e:
        log.critical(f"Failed to read from database: {e}")
        
        conn.close()
        sys.exit(1)
        
def dbUpdateCheck(rLastname, rFirstname):
    log.info("dbUpdateCheck invoked")
    global conn
    cursor = conn.cursor()
    try:
        query = "UPDATE `customers` SET `LastName` = %s WHERE LastName = %s"
        cursor.execute(query, (rFirstname, rLastname))
        conn.commit()
        log.info("%d record(s) affected", cursor.rowcount)
        dbDeleteCheck(rFirstname)
    except Exception as e:
        log.critical(f"Failed to update database: {e}")
        
        conn.close()
        sys.exit(1)
        
def dbDeleteCheck(rFirstname):
    log.info("dbDeleteCheck invoked")
    global conn
    cursor = conn.cursor()
    try:
        query = "DELETE FROM `customers` WHERE FirstName=%s"
        cursor.execute(query, (rFirstname,))
        conn.commit()
        log.info("%d record(s) affected", cursor.rowcount)
    except Exception as e:
        log.critical(f"Failed to delete from database: {e}")
        conn.close()
        sys.exit(1)
    finally:
        quit()
        
def randomNameGenerator():
    log.info("RandomNameGenerator invoked")
    lastnameLength = 8
    firstnameLength = 5
    emailHostLength = 8
    emailTLD = ".invalid"
    telephoneLength = 10

    randTelephone = str(''.join(random.choices(string.digits, k=telephoneLength)))
    randFirstname = str(''.join(random.choices(string.ascii_lowercase, k=firstnameLength)))
    randLastname = str(''.join(random.choices(string.ascii_lowercase, k=lastnameLength)))
    randEmailHost = str(''.join(random.choices(string.ascii_lowercase, k=emailHostLength)))
    randEmail = str(randFirstname) + "@" + str(randEmailHost) + str(emailTLD)
    return randLastname, randFirstname, randEmail, randTelephone 

def quit():
    conn.close()
    sys.exit(0)
    
if __name__ == "__main__":
    log.info("Program started")
    main()
