import os
import logging as log 
import argparse
import mysql.connector as sql

workingDir = os.getcwd()
dbcredPath = os.path.join(workingDir, "dbcred")

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode (debugging)")
args = parser.parse_args()

if args.verbose:
    log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)
    log.basicConfig(level=log.DEBUG)
    log.debug("Verbose mode invoked.")
else:
    log.basicConfig(format='', level=log.CRITICAL)

def initDBcred():
    log.info("initDBcred invoked")
    if os.path.exists(dbcredPath):
        log.info("dbcred found")
        dbConnectCheck()
    else:
        log.warning("dbcred NOT found")
        readPermissionCheck()
        
def readPermissionCheck():
    log.info("readPermissionCheck invoked")
    if os.access(workingDir, os.R_OK):
        log.info("Read permissions granted")
        readPermission = True
        dbcredCreate()
    else:
        log.error("Read permissions not granted.")
        readPermission = False
        print(f"[CRITICAL] Read permissions are not granted for the directory: {workingDir}")
        return 1
    
def dbcredUserInput():
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
        
def writePermissionCheck():
    log.info("writePermissionCheck invoked")
    if os.access(workingDir, os.W_OK):
        log.info("Write permissions granted")
        readPermission = True
        dbcredCreate()
    else:
        log.error("Write permissions not granted.")
        readPermission = False
        print(f"[CRITICAL] Write permissions are not granted for the directory: {workingDir}")
        return 1

def dbcredCreate():
    log.info("dbcredCreate invoked")
        
def dbConnectCheck():
    log.info("dbConnectCheck invoked")
    with open(dbcredPath) as dbcred:
        credentials = dbcred.read()
        credentials = credentials.strip()
        creds_dict = {}
    for item in credentials.split(','):     
        key, value = item.split('=')
        creds_dict[key.strip()] = value.strip().strip("'")
    dbcred = open(dbcredPath)
    database = sql.connect(host=creds_dict['host'], port=int(creds_dict['port']), user=creds_dict['user'], password=creds_dict['password'], database=creds_dict['database'])
    print(database)

if __name__ == "__main__":
    initDBcred()