import mysql.connector as sql
import os

workingDir = os.getcwd()
dbcredPath = os.path.join(workingDir, "dbcred")
dbcred = open(dbcredPath)

with open(dbcredPath) as dbcred:
    credentials = dbcred.read()
    credentials = credentials.strip()

# Convert the credentials string to a dictionary
creds_dict = {}
for item in credentials.split(','):
    key, value = item.split('=')
    creds_dict[key.strip()] = value.strip().strip("'")

# Connect to the database using the parsed credentials
dbstatus = sql.connect(
    host=creds_dict['host'],
    port=int(creds_dict['port']),
    user=creds_dict['user'],
    password=creds_dict['password'],
    database=creds_dict['database']
)

print(dbstatus)