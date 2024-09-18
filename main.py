import os
import logging as log
import argparse
import mysql.connector as sql
import random
import string
from tabulate import tabulate as tab
import asyncio ## debugging

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
    readPermission = readPermissionCheck()
    if readPermission == True:
        initDBcred()
    else:
        print("Fatal error")
        return

def initDBcred():
    log.info("initDBcred invoked")
    if os.path.exists(dbcredPath):
        log.info("dbcred found")
        dbWriteCheck()
    else:
        log.warning("dbcred NOT found")
        dbcredMenu()

def dbcredMenu():
    log.info("dbcredUserInput invoked")
    while True:
        userInput = input("Do you want to create the database credential file? (yes/no): ")
        if userInput.lower() in ["yes", "y"]:
            log.info("User input YES to creating dbcred")
            writePermissionCheck()
            break
        elif userInput.lower() in ["no", "n"]:
            log.info("User input NO to creating dbcred")
            print("Exiting...")
            break
        else:
            log.warning("Are you serious?")
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
        return readPermission
    
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
        return writePermission


def dbcredCreate():
    log.info("dbcredCreate invoked")


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
    log.info("dbConnectCheck invoked")
    creds_dict = parseCredentials()
    conn = sql.connect(
        host=creds_dict["host"],
        port=int(creds_dict["port"]),
        user=creds_dict["user"],
        password=creds_dict["password"],
        database=creds_dict["database"],
    )
    log.info(conn)
    return conn


def dbWriteCheck():
    log.info("dbWriteCheck invoked")
    randomData = randomNameGenerator()
    rLastname = randomData[0]
    rFirstname = randomData[1]
    rEmail = randomData[2]
    rTelephone = randomData[3]
    conn = dbConn()
    cursor = conn.cursor() 
    try:
        query = "INSERT INTO `customers` (`LastName`, `FirstName`, `Email`, `Telephone`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (rLastname, rFirstname, rEmail, rTelephone))
        conn.commit()
        log.info("Data written to Database")
    finally:
        dbReadCheck()


def dbReadCheck():
    log.info("dbReadCheck invoked")
    conn = dbConn()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM `customers`"
        cursor.execute(query)
        queryResult = cursor.fetchall()
        headers = ['ID', 'Last Name', 'First Name', 'Email', 'Phone']
        for res in queryResult:
            print(tab(res, headers=headers, tablefmt='grid'))
    finally:
        sleep()
        
def randomNameGenerator():
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

def sleep(): # debug
    input("Press any key to continue")
    
if __name__ == "__main__":
    log.info("Program started")
    main()
