import os
import logging as log
import argparse
import mysql.connector as sql

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
        wait()
    else:
        print("Fatal error")
        return

def initDBcred():
    log.info("initDBcred invoked")
    if os.path.exists(dbcredPath):
        log.info("dbcred found")
        wait()
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
    conn = dbConn()
    log.info("dbWriteCheck invoked")
    cursor = conn.cursor()  # Create the cursor manually
    try:
        # Input from the user
        LastName = input("Insert last name: ")
        FirstName = input("Insert first name: ")
        Email = input("Insert email: ")
        Telephone = input("Insert telephone: ")

        # Correct SQL query with placeholders for values
        query = "INSERT INTO `customers` (`LastName`, `FirstName`, `Email`, `Telephone`) VALUES (%s, %s, %s, %s)"

        # Executing the query and passing the user input as a tuple
        cursor.execute(query, (LastName, FirstName, Email, Telephone))

        # Commit the transaction
        conn.commit()
        log.info("Data written to Database")
    finally:
        dbReadCheck()


def dbReadCheck():
    log.info("dbReadCheck invoked")

def wait():
    input("Press Enter to exit...")

if __name__ == "__main__":
    log.info("Program started")
    main()
